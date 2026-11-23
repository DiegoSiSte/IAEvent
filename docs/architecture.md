# Arquitectura — FACEBOT

## Tipo

Cliente-servidor modular (S4 SYSTEM ARCHITECTURE).

### Backend (S4 Backend responsibilities)

- `backend/main.py` — app FastAPI (entrada).
- `backend/api/routes.py`, `backend/api/schemas.py` — REST API y esquemas Pydantic (S7).
- `backend/database/repository.py`, `backend/database/profiles.json` — perfiles e inscripción (S8).
- `backend/services/session_service.py` — estado visible de la sesión (S7).
- `backend/services/recommendation.py` — recomendaciones por intereses (S2 obj. 7).
- `backend/camera/camera_service.py` — estado de la cámara (base, S7; M5 - Yamil).
- `backend/recognition/face_service.py` — esquema de detección/inscripción/reconocimiento (base, S5; M5 - Yamil).

### Frontend (S4 Frontend responsibilities)

- `frontend/main.py` — app shell Flet (skeleton inicial; M3/M4).
- `frontend/screens/` — welcome, waiting, processing, recognized, unknown (skeletons; M3 Ashly).
- `frontend/components/` — profile_card, interest_card, recommendation_card (skeletons; M3 Ashly).
- `frontend/services/api_client.py` — cliente HTTPX al backend (M4 Rafael).

### Flujo de datos

`cámara → face_service → repository (perfiles+consent, S10) → session_service/recommendation → REST API → frontend (screens/components, S4) → POST /api/session/reset`.

### Reglas clave

- El frontend nunca accede a `profiles.json` directamente (S4).
- El backend es el único que accede a la base de datos (S4).
- No se exponen biometrías ni imágenes faciales por la API (S10).
- Solo se identifica a participantes inscritos y consensuados (S10).

Ver [docs/api_contract.md](api_contract.md) para los endpoints.
