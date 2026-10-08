from fastapi.testclient import TestClient
from humanos.api import app

client=TestClient(app)

def test_routes():
    for path in ['/signals','/moments','/cohorts']:
        assert client.get(path).status_code==200

def test_bad_dimension():
    assert client.get('/cohorts/unknown/value').status_code==400

def test_unknown_cohort():
    assert client.get('/cohorts/role/unknown').status_code==404
