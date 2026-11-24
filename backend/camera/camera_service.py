"""Servicio de cámara (base, M5 - Yamil).

Estado de la cámara + captura de frames con OpenCV (§5, §4 backend).
Manejo de desconección (§5).
"""

from typing import Any, Dict, Optional

import cv2


class CameraService:
    """Controla la cámara inicial (USB, §9): disponibilidad y captura."""

    def __init__(self, source: int = 0) -> None:
        self.source = int(source)

    def status(self) -> Dict[str, Any]:
        """Devuelve {'status': 'connected'|'disconnected', 'camera_available': bool}."""
        try:
            capture = cv2.VideoCapture(self.source)
            try:
                available = bool(capture.isOpened())
            finally:
                capture.release()
        except Exception:
            available = False
        return {"status": "connected" if available else "disconnected", "camera_available": available}

    def capture_frame(self) -> Optional[Any]:
        """Captura un frame de la cámara; devuelve None si no hay cámara/dispositivo."""
        try:
            capture = cv2.VideoCapture(self.source)
            try:
                ret, frame = capture.read()
            finally:
                capture.release()
        except Exception:
            return None
        return frame if ret else None


_camera = CameraService()


def get_status() -> Dict[str, Any]:
    """Estado de la cámara (§7 GET /api/camera/status)."""
    return _camera.status()


def capture_frame() -> Optional[Any]:
    """Captura un frame (§2 obj. 3). None si no hay cámara."""
    return _camera.capture_frame()
