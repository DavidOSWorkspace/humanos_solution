"""Option A: reproducible Wave 2 regression, with held-out test and CV on train only."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ['learning_appetite_w1','learning_capacity_w1','development_access_w1',
           'professional_agency_w1','knowledge_exchange_w1','future_visibility_w1']
CATEGORICAL = ['age_group','role','work_mode']
TARGET = 'future_visibility_w2'

def validate_predictive(df):
    needed = ['participant_id', *NUMERIC, *CATEGORICAL, TARGET]
    if not set(needed).issubset(df.columns):
        raise ValueError('Missing predictive columns')
    if df[needed].isna().any().any() or df.participant_id.duplicated().any():
        raise ValueError('Missing values or duplicate participant IDs')
    for col in [*NUMERIC, TARGET]:
        if not pd.api.types.is_numeric_dtype(df[col]) or not np.isfinite(df[col]).all() or not df[col].between(0,100).all():
            raise ValueError(f'Invalid 0-100 scores: {col}')

def pipeline(model):
    return Pipeline([('preprocess', ColumnTransformer([
        ('numeric', StandardScaler(), NUMERIC),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL)])),
        ('model', model)])

def evaluate(y, pred):
    return {'mae': round(float(mean_absolute_error(y,pred)),3),
            'rmse': round(float(np.sqrt(mean_squared_error(y,pred))),3),
            'r2': round(float(r2_score(y,pred)),3)}

def run(csv_path, output_dir=None):
    df = pd.read_csv(csv_path)
    validate_predictive(df)
    X, y = df[NUMERIC+CATEGORICAL], df[TARGET]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=42)
    models = {
        'baseline': DummyRegressor(strategy='mean'),
        'ridge': pipeline(Ridge(alpha=1.0)),
        'random_forest': pipeline(RandomForestRegressor(n_estimators=150, min_samples_leaf=3, random_state=42, n_jobs=1)),
        'gradient_boosting': pipeline(GradientBoostingRegressor(random_state=42))}
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    report = {'dataset_rows':len(df), 'train_rows':len(Xtr), 'test_rows':len(Xte), 'target':TARGET,
              'model_results':{}}
    fitted = {}
    for name, model in models.items():
        # Validation is performed on TRAIN only; test stays untouched until final assessment.
        scores = cross_validate(model, Xtr, ytr, cv=cv,
                                scoring={'mae':'neg_mean_absolute_error','r2':'r2'}, n_jobs=1)
        model.fit(Xtr,ytr)
        report['model_results'][name] = {
            'cv_train_mae':round(float(-scores['test_mae'].mean()),3),
            'cv_train_r2':round(float(scores['test_r2'].mean()),3),
            'train':evaluate(ytr,model.predict(Xtr)),
            'test':evaluate(yte,model.predict(Xte))}
        fitted[name] = model
    # Preselect Ridge for interpretability and regularization, regardless of held-out test scores.
    chosen = fitted['ridge']
    perm = permutation_importance(chosen, Xte, yte, n_repeats=20, random_state=42,
                                  scoring='neg_mean_absolute_error')
    report['ridge_permutation_mae_improvement'] = {
        col:round(float(v),3) for col,v in zip(Xte.columns,perm.importances_mean)}
    predictions = Xte[['future_visibility_w1']].copy()
    predictions['actual_w2'] = yte
    predictions['predicted_w2'] = np.clip(chosen.predict(Xte),0,100)
    predictions['estimated_change'] = predictions['predicted_w2']-predictions['future_visibility_w1']
    predictions['estimated_decline'] = predictions['estimated_change'] < 0
    if output_dir is not None:
        output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
        (output_dir/'predictive_metrics.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
        predictions.to_csv(output_dir/'predictions_test.csv',index=False)
    return report, predictions

if __name__=='__main__':
    base=Path(__file__).resolve().parents[2]
    report,_=run(base/'data'/'predictive_challenge.csv',base/'outputs')
    print(json.dumps(report,indent=2,ensure_ascii=False))
