"""Tests del servicio de reconocimacial (M5 - Diego).

Uso de imágenes sintéticas: sin cámara real (§10: datos sintéticos para pruebas).
"""

import numpy as np

from backend.database.repository import ProfileRepository
from backend.recognition.face_service import FaceService
from backend.services.session_service import SessionService, recognition_cycle


def _synthetic_face(half: str) -> np.ndarray:
    """Rostro sintético: mitad izquierda o derecha blanca (para distinción)."""
    face = np.zeros((80, 80, 3), dtype=np.uint8)
    if half == "left":
        face[:, :40] = 200
    elif half == "right":
        face[:, 40:] = 200
    return face


class _FakeDetector:
    """Detector falso: detecta un "rostro" que cubre el frame sintético."""

    def detectMultiScale(self, gray, scaleFactor=None, minNeighbors=None, minSize=None):
        height, width = gray.shape
        return [(0, 0, width, height)]


def _service() -> FaceService:
    return FaceService(detector=_FakeDetector(), confidence_threshold=0.6)


def test_enroll_and_recognize_same_face():
    service = _service()
    face = _synthetic_face("left")
    assert service.enroll("USR001", face) is True
    assert service.recognize_face(face) == "USR001"


def test_not_enrolled_returns_none():
    service = _service()
    assert service.recognize_face(_synthetic_face("left")) is None


def test_different_face_returns_none():
    service = _service()
    service.enroll("USR001", _synthetic_face("left"))
    assert service.recognize_face(_synthetic_face("right")) is None


def test_enroll_is_idempotent():
    service = _service()
    face = _synthetic_face("left")
    assert service.enroll("USR001", face) is True
    assert service.enroll("USR001", face) is False
    assert service.is_enrolled("USR001") is True


def test_consent_checker_denies_recognition():
    service = _service()
    service.enroll("USR001", _synthetic_face("left"))
    assert service.recognize_face(_synthetic_face("left"), consent_checker=lambda pid: False) is None


def test_enroll_if_consented_checks_consent():
    service = _service()
    face = _synthetic_face("left")
    assert service.enroll_if_consented("USR001", face, consent_checker=lambda pid: True) is True
    assert service.is_enrolled("USR001") is True
    assert service.enroll_if_consented("USR002", face, consent_checker=lambda pid: False) is False
    assert not service.is_enrolled("USR002")


def test_recognize_frame_matches_enrolled():
    service = _service()
    face = _synthetic_face("left")
    service.enroll("USR001", face)
    assert service.recognize(_synthetic_face("left")) == "USR001"


def test_recognize_frame_without_enrollment_returns_none():
    service = _service()
    service.enroll("USR001", _synthetic_face("left"))
    assert service.recognize(_synthetic_face("right")) is None


def test_reset_clears_templates():
    service = _service()
    face = _synthetic_face("left")
    service.enroll("USR001", face)
    service.reset()
    assert not service.is_enrolled("USR001")
    assert service.recognize_face(face) is None


class _FrameCamera:
    def capture_frame(self):
        return _synthetic_face("left")


class _NoCamera:
    def capture_frame(self):
        return None


def test_recognition_cycle_recognizes_consented_user():
    repository = ProfileRepository()
    session = SessionService()
    face = _service()
    face.enroll("USR001", _synthetic_face("left"))
    recognition_cycle(_FrameCamera(), face, repository, session)
    status, person = session.status()
    assert status == SessionService.RECOGNIZED
    assert person["id"] == "USR001"
    assert person["name"] == "Carlos"


def test_recognition_cycle_unknown_when_not_enrolled():
    repository = ProfileRepository()
    session = SessionService()
    face = _service()
    recognition_cycle(_FrameCamera(), face, repository, session)
    status, person = session.status()
    assert status == SessionService.UNKNOWN
    assert person is None


def test_recognition_cycle_waiting_without_frame():
    repository = ProfileRepository()
    session = SessionService()
    face = _service()
    recognition_cycle(_NoCamera(), face, repository, session)
    status, person = session.status()
    assert status == SessionService.WAITING


def test_recognition_cycle_unknown_without_consent():
    repository = ProfileRepository()
    session = SessionService()
    face = _service()
    face.enroll("USR003", _synthetic_face("left"))  # USR003 no tiene consent (§8, §10).
    recognition_cycle(_FrameCamera(), face, repository, session)
    status, _ = session.status()
    assert status == SessionService.UNKNOWN
