"""Automated tests for the student-ml-api Flask application."""

import pytest

from app import APP_VERSION, app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "wrong"
    assert data["application"] == "student-ml-api"
    assert data["version"] == APP_VERSION


def test_predict_success(client):
    response = client.post("/predict", json={"value": 10})
    data = response.get_json()

    assert response.status_code == 200
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_predict_missing_input(client):
    response = client.post("/predict", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_predict_invalid_input(client):
    response = client.post("/predict", json={"value": "not-a-number"})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_predict_negative_value(client):
    response = client.post("/predict", json={"value": -5})
    data = response.get_json()

    assert response.status_code == 200
    assert data["prediction"] == -10
