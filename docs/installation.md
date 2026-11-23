# Instalación — FACEBOT

Requisitos: Python 3.11+, Git, webcam USB (target inicial, S9).

## 1. Entorno virtual y dependencias

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` incluye FastAPI, Uvicorn, OpenCV, Pydantic, Pytest, HTTPX y Flet (S3); las versiones están pinneadas según la última versión estable de PyPI.

## 2. Configuración local

```bash
copy .env.example .env
```

Edita `.env`: `HOST`, `PORT`, `API_BASE_URL` (URL local del backend, sin IP hardcodeada, S9) y `CAMERA_SOURCE` (S9).

## 3. Iniciar el backend

```bash
.venv\Scripts\uvicorn backend.main:app
```

(O `uvicorn backend.main:app` desde la raíz del proyecto.)

## 4. Pruebas iniciales

```bash
.venv\Scripts\python -m pytest
```

## 5. Base actual del proyecto

- Backend funcional: endpoints `GET /api/status`, `GET /api/camera/status`, `GET /api/session`, `GET /api/person/{id}`, `POST /api/session/reset` (S7).
- Skeleton del frontend (`frontend/`): implementación visual (Ashly, M3; API: Rafael, M4).
- Reconocimiento facial: skeleton en `backend/recognition/face_service.py` (implementación: Yamil, M5).
