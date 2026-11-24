"""Tests iniciales del API (S15: Definition of Done — relevant tests pass)."""

import base64

import cv2
import numpy as np
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


def test_recognition_scan_without_camera_is_controlled():
    response = client.post("/api/recognition/scan")
    assert response.status_code in {200, 503}


def test_enrollment_rejects_participant_without_consent():
    response = client.post(
        "/api/recognition/enroll/USR003",
        json={"image_base64": "not-an-image"},
    )
    assert response.status_code == 404


def test_enrollment_accepts_image_for_consented_participant(monkeypatch):
    image = np.zeros((80, 80, 3), dtype=np.uint8)
    encoded_ok, encoded = cv2.imencode(".png", image)
    assert encoded_ok
    image_base64 = base64.b64encode(encoded.tobytes()).decode("ascii")
    monkeypatch.setattr(
        "backend.recognition.face_service.enroll_participant",
        lambda profile_id, frame: 1,
    )

    response = client.post(
        "/api/recognition/enroll/USR001",
        json={"image_base64": image_base64},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "enrolled",
        "profile_id": "USR001",
        "template_count": 1,
    }
