"""HTTP client del frontend → backend (S4 comunicación). (Rafael, M4)"""

import base64
import os
from typing import Any

import httpx


def default_base_url() -> str:
    """URL base del backend desde API_BASE_URL (S9)."""
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


class FacebotApiClient:
    """Cliente HTTPX para la API REST del backend (S4).

    La comunicación frontend-backend se hace solo por endpoints HTTP (S4).
    """

    def __init__(self, base_url: str) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=5.0)

    def get_status(self) -> dict[str, Any]:
        """GET /api/status — disponibilidad del backend."""
        response = self._client.get("/api/status")
        response.raise_for_status()
        return response.json()

    def get_camera_status(self) -> dict[str, Any]:
        response = self._client.get("/api/camera/status")
        response.raise_for_status()
        return response.json()

    def get_session(self) -> dict[str, Any]:
        """GET /api/session — estado actual de la sesión."""
        response = self._client.get("/api/session")
        response.raise_for_status()
        return response.json()

    def scan_recognition(self) -> dict[str, Any]:
        response = self._client.post("/api/recognition/scan")
        if response.status_code == 503:
            return {"status": "error", "detail": "Camera unavailable"}
        response.raise_for_status()
        return response.json()

    def enroll_participant(self, profile_id: str, image_bytes: bytes) -> dict[str, Any]:
        """Envía una imagen seleccionada para generar su plantilla facial local."""
        encoded_image = base64.b64encode(image_bytes).decode("ascii")
        response = self._client.post(
            f"/api/recognition/enroll/{profile_id}",
            json={"image_base64": encoded_image},
        )
        response.raise_for_status()
        return response.json()

    def reset_session(self) -> dict[str, Any]:
        """POST /api/session/reset — volver a waiting."""
        response = self._client.post("/api/session/reset")
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Cierra el cliente HTTP."""
        self._client.close()
