"""Pydantic schemas for the FACEBOT REST API (contract: docs/api_contract.md)."""

from typing import List, Optional

from pydantic import BaseModel


class Recommendation(BaseModel):
    """Recomendación de un proyecto universitario (S7 / S8)."""

    title: str
    description: str
    category: str


class PersonProfile(BaseModel):
    """Perfil público de un participante identificado (S7 GET /api/session)."""

    id: str
    name: str
    career: str
    interests: List[str]
    recommendations: List[Recommendation]


class StatusResponse(BaseModel):
    """Disponibilidad del backend (S7 GET /api/status)."""

    status: str
    application: str


class CameraStatusResponse(BaseModel):
    """Estado de la cámara (S7 GET /api/camera/status)."""

    status: str
    camera_available: bool


class SessionStateResponse(BaseModel):
    """Estado de la sesión (S7 GET /api/session)."""

    status: str
    person: Optional[PersonProfile] = None
