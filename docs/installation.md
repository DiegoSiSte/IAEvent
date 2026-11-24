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
.venv\Scripts\uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

(O `uvicorn backend.main:app` desde la raíz del proyecto.)

## 4. Pruebas iniciales

```bash
.venv\Scripts\python -m pytest
```

## 5. Ejecutar el frontend

```bash
.venv\Scripts\python frontend\main.py
```

El frontend usa `API_BASE_URL`. En la bienvenida, **Inscribir participante**
abre la pantalla de inscripción: escribe un ID que tenga `consent: true` en
`backend/database/profiles.json`, confirma la autorización y selecciona una
foto JPG o PNG (máximo 8 MB, un rostro visible). Después, **Comenzar** lleva a
la pantalla de espera y **Escanear** usa la cámara conectada al backend.

## 6. Inscripción facial

Antes de reconocer a una persona, debe existir su perfil consentido en
`backend/database/profiles.json`. La inscripción puede hacerse por API:

```text
POST /api/recognition/enroll/{profile_id}
{"image_base64":"<imagen JPEG o PNG codificada>"}
```

Las plantillas faciales se almacenan localmente en `.face_templates/` y no se
exponen por la API. Para eliminarlas:

```text
DELETE /api/recognition/{profile_id}
```
