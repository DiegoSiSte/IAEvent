"""Pydantic schemas for the FACEBOT REST API (contract: docs/api_contract.md)."""

from typing import List, Optional

from pydantic import BaseModel


class Recommendation(BaseModel):
    """Recomendación de un proyecto universitario (§7 / §8)."""

    title: str
    description: str
    category: str


class PersonProfile(BaseModel):
    """Perfil público de un participante identificado (§7 GET /api/session)."""

    id: str
    name: str
    career: str
    interests: List[str]
    recommendations: List[Recommendation]


class StatusResponse(BaseModel):
    """Disponibilidad del backend (§7 GET /api/status)."""

    status: str
    application: str


class CameraStatusResponse(BaseModel):
    """Estado de la cámara (§7 GET /api/camera/status)."""

    status: str
    camera_available: bool


class SessionStateResponse(BaseModel):
    """Estado de la sesión (§7 GET /api/session)."""

    status: str
    person: Optional[PersonProfile] = None


class EnrollRequest(BaseModel):
    """Solicitud de inscripción de un rostro (§5, §10)."""

    image_base64: str


class EnrollResponse(BaseModel):
    """Respuesta de inscripción (§5, §10)."""

    status: str
    profile_id: str
    template_count: int
