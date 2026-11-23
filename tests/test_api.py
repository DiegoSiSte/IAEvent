"""Tests iniciales del API (S15: Definition of Done — relevant tests pass)."""

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_api_status_returns_online():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "application": "FACEBOT"}


def test_camera_status_shape():
    response = client.get("/api/camera/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"connected", "disconnected"}
    assert isinstance(data["camera_available"], bool)


def test_session_starts_waiting():
    response = client.get("/api/session")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "waiting"
    assert data["person"] is None


def test_session_reset_returns_waiting():
    response = client.post("/api/session/reset")
    assert response.status_code == 200
    assert response.json()["status"] == "waiting"


def test_person_endpoint_returns_public_profile():
    response = client.get("/api/person/USR001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "USR001"
    assert data["name"] == "Carlos"
    assert data["career"] == "Ingenieria de Sistemas"
    assert data["interests"]
    assert data["recommendations"]


def test_person_endpoint_rejects_non_consented():
    response = client.get("/api/person/USR003")
    assert response.status_code == 404


def test_person_endpoint_rejects_unknown():
    response = client.get("/api/person/USR999")
    assert response.status_code == 404
