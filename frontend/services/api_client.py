"""HTTP client del frontend → backend (S4 comunicación). (Rafael, M4)"""

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
        return self._client.get("/api/status").json()

    def get_session(self) -> dict[str, Any]:
        """GET /api/session — estado actual de la sesión."""
        return self._client.get("/api/session").json()

    def reset_session(self) -> dict[str, Any]:
        """POST /api/session/reset — volver a waiting."""
        return self._client.post("/api/session/reset").json()

    def close(self) -> None:
        """Cierra el cliente HTTP."""
        self._client.close()
