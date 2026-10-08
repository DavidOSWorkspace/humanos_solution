"""Deterministic scoring and cohort reporting for synthetic HumanOS data."""
import numpy as np
import pandas as pd

DIMENSIONS = ('age_group', 'role', 'work_mode')


def validate(responses: pd.DataFrame, config: pd.DataFrame) -> None:
    needed = {'participant_id', *DIMENSIONS}
    config_needed = {'item_code', 'signal', 'reverse_flag', 'weight'}
    if not needed.issubset(responses.columns):
        raise ValueError(f'Missing response metadata: {sorted(needed - set(responses.columns))}')
    if not config_needed.issubset(config.columns):
        raise ValueError(f'Missing config fields: {sorted(config_needed - set(config.columns))}')
    if responses.empty or config.empty:
        raise ValueError('Inputs cannot be empty')
    if responses.isna().any().any() or config[list(config_needed)].isna().any().any():
        raise ValueError('Missing values in responses/config')
    if responses.participant_id.duplicated().any():
        raise ValueError('Duplicate participant_id')
    if config.item_code.duplicated().any():
        raise ValueError('Duplicate item_code')
    if not config['reverse_flag'].map(lambda x: isinstance(x, (bool, np.bool_))).all():
        raise ValueError('reverse_flag must be boolean')
    if not pd.api.types.is_numeric_dtype(config.weight) or not np.isfinite(config.weight).all() or (config.weight <= 0).any():
        raise ValueError('All weights must be positive and finite')
    items = config.item_code.tolist()
    if not set(items).issubset(responses.columns):
        raise ValueError(f'Missing item columns: {sorted(set(items)-set(responses.columns))}')
    for item in items:
        col = responses[item]
        if not pd.api.types.is_numeric_dtype(col) or not np.isfinite(col).all() or not col.between(1, 5).all() or not (col % 1 == 0).all():
            raise ValueError(f'Invalid Likert responses in {item}; expected integers 1-5')


def calculate_signals(responses: pd.DataFrame, config: pd.DataFrame) -> pd.DataFrame:
    validate(responses, config)
    out = responses[['participant_id', *DIMENSIONS]].copy()
    for signal, group in config.groupby('signal', sort=True):
        cols = group.item_code.tolist()
        values = responses[cols].astype(float).copy()
        for _, item in group.iterrows():
            if item['reverse_flag']:
                values[item.item_code] = 6 - values[item.item_code]
        normalized = (values - 1) * 25
        out[signal] = np.average(normalized.to_numpy(), axis=1, weights=group.weight.to_numpy(dtype=float))
    return out


def organization_signals(scored: pd.DataFrame) -> list[dict]:
    signals = [c for c in scored.columns if c not in ('participant_id', *DIMENSIONS)]
    return [{'signal': s, 'n': len(scored), 'score': round(float(scored[s].mean()), 2)} for s in signals]


def moments(scored: pd.DataFrame) -> pd.DataFrame:
    """Non-exclusive heuristic affinity scores; not a validated psychometric instrument."""
    s = scored
    result = s[['participant_id']].copy()
    result['Learning / Exploration'] = .6*s['Learning Appetite'] + .4*s['Learning Capacity']
    result['Mastery / Contribution'] = .55*s['Knowledge Exchange'] + .45*s['Professional Agency']
    # Proxy for capacity to sustain current contribution, NOT a measurement of preference for stability.
    result['Consolidation / Stability'] = .5*s['Future Visibility'] + .3*s['Professional Agency'] + .2*s['Learning Capacity']
    # Exploratory proxy; no direct questionnaire item measures willingness to change career direction.
    result['Transition / Reinvention'] = .45*s['Learning Appetite'] + .35*s['Learning Capacity'] + .2*(100-s['Future Visibility'])
    return result


def cohort_report(scored: pd.DataFrame, min_n: int = 10) -> list[dict]:
    signals = [c for c in scored.columns if c not in ('participant_id', *DIMENSIONS)]
    rows = []
    for dimension in DIMENSIONS:
        for value, subset in scored.groupby(dimension, sort=True):
            n = len(subset)
            for signal in signals:
                # Hide scores and deltas for unreportable cohorts; n is still visible.
                rows.append({'dimension': dimension, 'value': str(value), 'signal': signal,
                             'n': n, 'reportable': bool(n >= min_n),
                             'score': round(float(subset[signal].mean()), 2) if n >= min_n else None,
                             'organization_score': round(float(scored[signal].mean()), 2),
                             'delta': round(float(subset[signal].mean()-scored[signal].mean()), 2) if n >= min_n else None})
    return rows
