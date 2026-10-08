"""FastAPI application. Run: uvicorn humanos.api:app --reload"""
from functools import lru_cache
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException
from .core import calculate_signals, organization_signals, moments, cohort_report, DIMENSIONS

app = FastAPI(title='HumanOS Intelligence Engine', version='1.0')
DATA_DIR = Path(__file__).resolve().parents[2] / 'data'

@lru_cache(maxsize=1)
def computed():
    scored = calculate_signals(pd.read_csv(DATA_DIR/'responses.csv'), pd.read_csv(DATA_DIR/'item_config.csv'))
    return scored, moments(scored), cohort_report(scored)

@app.get('/signals')
def signals_endpoint():
    scored, _, _ = computed()
    return {'organization': organization_signals(scored)}

@app.get('/moments')
def moments_endpoint():
    _, m, _ = computed()
    return {'method': 'Exploratory non-exclusive heuristic affinities (0-100); not validated categories',
            'organization': {c: round(float(m[c].mean()), 2) for c in m.columns if c != 'participant_id'}}

@app.get('/cohorts')
def cohorts_endpoint():
    return {'cohorts': computed()[2]}

@app.get('/cohorts/{dimension}/{value}')
def cohort_endpoint(dimension: str, value: str):
    if dimension not in DIMENSIONS:
        raise HTTPException(status_code=400, detail=f'dimension must be one of {DIMENSIONS}')
    matches = [r for r in computed()[2] if r['dimension'] == dimension and r['value'] == value]
    if not matches:
        raise HTTPException(status_code=404, detail='Cohort not found')
    return {'dimension': dimension, 'value': value, 'signals': matches}
