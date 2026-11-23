"""Servicio de reconocimiento facial — esquema base (S5, S4 backend). (M5 - Yamil)

Interfaz que define la API esperada: detección, inscripción con consent
y reconocimiento local (S10: solo participantes inscritos y consensuados).
La implementación llega en la M5.
"""

from typing import Any, List, Optional


def detect_faces(frame: Any) -> List[Any]:
    """Devuelve las ubicaciones de rostros detectados en un frame. (M5 - Yamil)"""
    raise NotImplementedError("detect_faces: pendiente de implementación (M5 - Yamil)")


def enroll_participant(profile_id: str) -> None:
    """Inscribe un participante consensuado. (M5 - Yamil)"""
    raise NotImplementedError("enroll_participant: pendiente de implementación (M5 - Yamil)")


def recognize(frame: Any) -> Optional[str]:
    """Devuelve el id del participante identificado o None (desconocido). (M5 - Yamil)"""
    raise NotImplementedError("recognize: pendiente de implementación (M5 - Yamil)")
