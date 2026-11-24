# Arquitectura — FACEBOT

## Tipo

Cliente-servidor modular (§4 SYSTEM ARCHITECTURE).

### Backend (§4 Backend responsibilities)

- `backend/main.py` — app FastAPI + ciclo de reconocimacial en segundo plano (§2 obj. 1-10).
- `backend/api/routes.py`, `backend/api/schemas.py` — REST API y esquemas Pydantic (§7).
- `backend/database/repository.py`, `backend/database/profiles.json` — perfiles e inscripción (§8).
- `backend/services/session_service.py` — estado visible de la sesión + ciclo de reconocimacial (§7, §2 obj. 5).
- `backend/services/recommendation.py` — recomendaciones por intereses (§2 obj. 7).
- `backend/camera/camera_service.py` — estado + captura de frames de la cámara (§5, §2 obj. 1-3).
- `backend/recognition/face_service.py` — detección (Haar cascade), inscripción y reconocimacial por similitud (M5 - Diego, §10).

### Frontend (§4 Frontend responsibilities)

- `frontend/main.py` — app shell Flet: Welcome → Waiting → (Processing | Recognized | Unknown), polling de sesión (§4, §7).
- `frontend/screens/` — welcome, waiting, processing, recognized, unknown (§4, §2 obj. 9).
- `frontend/components/` — profile_card, interest_card, recommendation_card (§4, §2 obj. 9).
- `frontend/services/api_client.py` — cliente HTTPX al backend (M4 Rafael).

### Flujo de datos (§4)

`cámara → camera_service.capture_frame() → face_service.recognize() → repository.get_profile() (consent) → session_service.set_recognized() → GET /api/session → frontend (RecognizedScreen/UnknownScreen) → POST /api/session/reset → Welcome`.

### Reglas clave (§10)

- El frontend nunca accede a `profiles.json` directamente (§4).
- El backend es el único que accede a la base de datos (§4).
- No se exponen biometrías ni imágenes faciales por la API (§10).
- Solo se identifica a participantes inscritos y consensuados (§10).
- La sesión se resetea tras la interacción (§10).
