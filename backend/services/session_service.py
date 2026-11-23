"""Servicio de sesión: estado visible de la interacción (S7)."""

from threading import Lock
from typing import Any, Dict, Optional, Tuple


class SessionService:
    """Estado de la sesión: waiting, processing, recognized, unknown, error (S7)."""

    WAITING = "waiting"
    PROCESSING = "processing"
    RECOGNIZED = "recognized"
    UNKNOWN = "unknown"
    ERROR = "error"

    def __init__(self) -> None:
        self._lock = Lock()
        self._status = self.WAITING
        self._person: Optional[Dict[str, Any]] = None

    def status(self) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Devuelve (status, person) del estado actual (S7 GET /api/session)."""
        with self._lock:
            return self._status, self._person

    def set(self, status: str, person: Optional[Dict[str, Any]] = None) -> None:
        """Define el estado (M5 usará processing/recognized/unknown/error)."""
        with self._lock:
            self._status = status
            self._person = person if status == self.RECOGNIZED else None

    def set_recognized(self, person: Dict[str, Any]) -> None:
        """Estado recognized con el perfil del participante (S7)."""
        self.set(self.RECOGNIZED, person)

    def reset(self) -> None:
        """Volver a waiting (S10, regla 10)."""
        self.set(self.WAITING)
