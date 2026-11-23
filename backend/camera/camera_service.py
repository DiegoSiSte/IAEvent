"""Servicio de cámara — base inicial (S5, S4 backend). (M5 - Yamil)

La captura de frames y el flujo de reconocimiento vienen en la M5;
este módulo define la base: disponibilidad + manejo de desconexión.
"""

from typing import Any, Dict

import cv2


class CameraService:
    """Reporta disponibilidad de la cámara (configurable por CAMERA_SOURCE, S9)."""

    def __init__(self, source: int = 0) -> None:
        self.source = int(source)

    def status(self) -> Dict[str, Any]:
        """Devuelve {'status': 'connected'|'disconnected', 'camera_available': bool}.

        Maneja desconexión/dispositivo ausente (S5: manejar desconexión).
        """
        try:
            capture = cv2.VideoCapture(self.source)
            try:
                available = bool(capture.isOpened())
            finally:
                capture.release()
        except Exception:
            available = False
        return {"status": "connected" if available else "disconnected", "camera_available": available}


_camera = CameraService()


def get_status() -> Dict[str, Any]:
    """Estado de la cámara (S7 GET /api/camera/status)."""
    return _camera.status()
