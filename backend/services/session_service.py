"""Servicio de sesión: estado visible de la interacción (§7).

M5 (Diego): ciclo de reconocimacial que actualiza la sesión a partir de
la cámara: waiting / processing / recognized / unknown / error.
"""

from threading import Lock
from typing import Any, Callable, Dict, Optional, Tuple

from backend.services.recommendation import build_recommendations


class SessionService:
    """Estado de la sesión: waiting, processing, recognized, unknown, error (§7)."""

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
        """Devuelve (status, person) del estado actual (§7 GET /api/session)."""
        with self._lock:
            return self._status, self._person

    def set(self, status: str, person: Optional[Dict[str, Any]] = None) -> None:
        """Define el estado (M5 usará processing/recognized/unknown/error)."""
        with self._lock:
            self._status = status
            self._person = person if status == self.RECOGNIZED else None

    def set_recognized(self, person: Dict[str, Any]) -> None:
        """Estado recognized con el perfil del participante (§7)."""
        self.set(self.RECOGNIZED, person)

    def reset(self) -> None:
        """Volver a waiting (§10, regla 10)."""
        self.set(self.WAITING)


def recognition_cycle(camera_service, face_service, repository, session_service) -> None:
    """Ciclo del flujo de reconocimacial (§2 obj. 3-5, §10).

    - Sin frame (cámara desconectada): waiting (§2 obj. 1).
    - Frame sin identificación segura: unknown (§2 obj. 10).
    - Participante consensuado identificado: recognized con perfil público
      y recomendaciones por intereses (§2 obj. 6, §7).
    """
    frame = camera_service.capture_frame()
    if frame is None:
        session_service.set(SessionService.WAITING)
        return
    session_service.set(SessionService.PROCESSING)
    consent_checker: Callable[[str], bool] = (
        lambda profile_id: repository.get_profile(profile_id) is not None
    )
    profile_id = face_service.recognize(frame, consent_checker=consent_checker)
    if not profile_id:
        session_service.set(SessionService.UNKNOWN)
        return
    profile = repository.get_profile(profile_id)
    if profile is None:
        session_service.set(SessionService.UNKNOWN)
        return
    if not profile.get("recommendations"):
        profile["recommendations"] = build_recommendations(profile.get("interests", []))
    session_service.set_recognized(profile)
