"""Tests del servicio de cámara (M5 base - TODO:Said, T15)."""

from backend.camera.camera_service import CameraService


def test_status_without_camera_reports_unavailable():
    camera = CameraService(source=99)
    status = camera.status()
    assert status["status"] in {"connected", "disconnected"}
    assert isinstance(status["camera_available"], bool)


def test_capture_frame_without_camera_returns_none():
    camera = CameraService(source=99)
    assert camera.capture_frame() is None
