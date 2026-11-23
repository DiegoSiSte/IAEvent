"""REST API routes — contrato definido en docs/api_contract.md (S7)."""

from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    CameraStatusResponse,
    PersonProfile,
    SessionStateResponse,
    StatusResponse,
)
from backend.database.repository import ProfileRepository
from backend.services.recommendation import build_recommendations
from backend.services.session_service import SessionService

router = APIRouter()

repository = ProfileRepository()
session_service = SessionService()


@router.get("/api/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    """GET /api/status — disponibilidad del backend (S7)."""
    return StatusResponse(status="online", application="FACEBOT")


@router.get("/api/camera/status", response_model=CameraStatusResponse)
def get_camera_status() -> CameraStatusResponse:
    """GET /api/camera/status — estado de la cámara (S7; cámara USB, S9)."""
    from backend.camera.camera_service import get_status

    info = get_status()
    return CameraStatusResponse(status=info["status"], camera_available=info["camera_available"])


@router.get("/api/session", response_model=SessionStateResponse)
def get_session() -> SessionStateResponse:
    """GET /api/session — estado: waiting/processing/recognized/unknown/error (S7)."""
    status, person = session_service.status()
    return SessionStateResponse(status=status, person=person)


@router.get("/api/person/{profile_id}", response_model=PersonProfile)
def get_person(profile_id: str) -> PersonProfile:
    """GET /api/person/{id} — perfil público de un participante inscrito (S7)."""
    profile = repository.get_profile(profile_id)
    if profile is None:
        # Desconocido o sin consentimiento: no se expone ni se identifica (S10).
        raise HTTPException(status_code=404, detail="Participant not found or has not consented")
    if not profile.get("recommendations"):
        profile["recommendations"] = build_recommendations(profile.get("interests", []))
    return PersonProfile(**profile)


@router.post("/api/session/reset", response_model=SessionStateResponse)
def reset_session() -> SessionStateResponse:
    """POST /api/session/reset — volver a waiting (S7, S10 regla 10)."""
    session_service.reset()
    status, person = session_service.status()
    return SessionStateResponse(status=status, person=person)
