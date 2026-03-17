import pytest
from fastapi.testclient import TestClient
from main import app, prediction

client = TestClient(app)


def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_prediction_endpoint():
    test_data = "How to perform unit testing in Python?"
    response = client.post('/predict', content=test_data)
    assert response.status_code == 200
    assert any([
        isinstance(response.json(), list),
        isinstance(response.json(), tuple)
    ])


def test_prediction_function():
    test_data = "How to perform unit testing in Python?"
    result = prediction(test_data)
    assert any([
        isinstance(result, list),
        isinstance(result, tuple)
    ])
    assert len(result) > 0
