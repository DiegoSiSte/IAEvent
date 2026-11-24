"""REST API routes — contrato definido en docs/api_contract.md (§7).

Endpoints adicionales (§2):
- POST /api/recognition/scan: escaneo de reconocimacial sobre demanda (§2 obj. 3).
- POST /api/recognition/enroll/{id}: inscripción de rostro, consent-aware (§5, §10).

Servicios compartidos (§4): cámara, reconocimacial (módulo), repositorio y
sesión — usados por la API, el ciclo de segundo plano (backend/main.py) y los
tests.
"""

import base64
import os
from typing import Optional

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    CameraStatusResponse,
    EnrollRequest,
    EnrollResponse,
    PersonProfile,
    SessionStateResponse,
    StatusResponse,
)
from backend.camera.camera_service import CameraService
from backend.database.repository import ProfileRepository
from backend.recognition import face_service
from backend.services.recommendation import build_recommendations
from backend.services.session_service import SessionService, recognition_cycle

router = APIRouter()

# Servicios compartidos (§4): configurables por variables de entorno (§9).
camera_service = CameraService(source=int(os.getenv("CAMERA_SOURCE") or "0"))
repository = ProfileRepository()
session_service = SessionService()


def _decode_image(image_base64: str) -> Optional[np.ndarray]:
    """Decodifica una imagen base64 a un frame BGR; None si es inválida."""
    try:
        raw = base64.b64decode(image_base64, validate=True)
        encoded = np.frombuffer(raw, dtype=np.uint8)
        frame = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    except Exception:
        return None
    return frame


@router.get("/api/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    """GET /api/status — disponibilidad del backend (§7)."""
    return StatusResponse(status="online", application="FACEBOT")


@router.get("/api/camera/status", response_model=CameraStatusResponse)
def get_camera_status() -> CameraStatusResponse:
    """GET /api/camera/status — estado de la cámara (§7; cámara USB, §9)."""
    info = camera_service.status()
    return CameraStatusResponse(status=info["status"], camera_available=info["camera_available"])


@router.get("/api/session", response_model=SessionStateResponse)
def get_session() -> SessionStateResponse:
    """GET /api/session — estado: waiting/processing/recognized/unknown/error (§7)."""
    status, person = session_service.status()
    return SessionStateResponse(status=status, person=person)


@router.get("/api/person/{profile_id}", response_model=PersonProfile)
def get_person(profile_id: str) -> PersonProfile:
    """GET /api/person/{id} — perfil público de un participante inscrito (§7)."""
    profile = repository.get_profile(profile_id)
    if profile is None:
        # Desconocido o sin consentimiento: no se expone ni se identifica (§10).
        raise HTTPException(status_code=404, detail="Participant not found or has not consented")
    if not profile.get("recommendations"):
        profile["recommendations"] = build_recommendations(profile.get("interests", []))
    return PersonProfile(**profile)


@router.post("/api/session/reset", response_model=SessionStateResponse)
def reset_session() -> SessionStateResponse:
    """POST /api/session/reset — volver a waiting (§7, §10 regla 10)."""
    session_service.reset()
    status, person = session_service.status()
    return SessionStateResponse(status=status, person=person)


@router.post("/api/recognition/scan", response_model=SessionStateResponse)
def recognition_scan() -> SessionStateResponse:
    """Desencadena un ciclo de reconocimacial sobre demanda (§2 obj. 3).

    Devuelve el estado de la sesión tras el escaneo (§7). Sin cámara, devuelve
    `waiting` (200): el escaneo está controlado y no se identifica forzadamente
    (§10).
    """
    if camera_service.capture_frame() is None:
        session_service.set(SessionService.WAITING)
    else:
        recognition_cycle(camera_service, face_service, repository, session_service)
    status, person = session_service.status()
    return SessionStateResponse(status=status, person=person)


@router.post("/api/recognition/enroll/{profile_id}", response_model=EnrollResponse)
def enroll_participant(profile_id: str, payload: EnrollRequest) -> EnrollResponse:
    """Inscribe la plantilla de un rostro de un participante consensuado (§5, §10).

    Respuesta: `{"status": "enrolled", "profile_id": ..., "template_count": N}`.
    404 si el participante no existe o no dio consent (§10).
    """
    if repository.get_profile(profile_id) is None:
        raise HTTPException(status_code=404, detail="Participant not found or has not consented")
    frame = _decode_image(payload.image_base64)
    template_count = face_service.enroll_participant(profile_id, frame)
    return EnrollResponse(status="enrolled", profile_id=profile_id, template_count=template_count)
