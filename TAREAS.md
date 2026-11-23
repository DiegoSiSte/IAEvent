# TAREAS — FACEBOT (proyecto IAEVENT)

> **Regla de orden:** esta lista define el orden de ejecución. Cuando una persona termina su tarea, la siguiente en la lista puede iniciar; **no hay tareas en paralelo**.

## Equipo

1. Said
2. Diego
3. Yamil
4. Rafael
5. Alcides

---

## Tarea 1 — Said — M1: Estructura del proyecto

Crear la estructura oficial del proyecto:

- Carpetas: `backend/api`, `backend/camera`, `backend/recognition`, `backend/database`, `backend/services`, `frontend/screens`, `frontend/components`, `frontend/services`, `tests`, `docs`.
- Archivos raíz: `README.md`, `requirements.txt`, `.gitignore`, `.env.example` (contenido sugerido: `HOST`, `PORT`, `API_BASE_URL`, `CAMERA_SOURCE`).

**Criterio de aceptación:** existe la estructura y `AGENTS.md` está en la raíz del proyecto.

## Tarea 2 — Diego — M1: Entorno de desarrollo y dependencias

- Crear el entorno virtual: `python -m venv .venv`.
- Instalar las dependencias estables: `fastapi`, `uvicorn`, `opencv-python`, `pydantic`, `pytest`, `httpx`.
- Verificar: `python -c "import fastapi, uvicorn, cv2, pydantic, httpx, pytest"`.

**Criterio de aceptación:** el entorno virtual funciona y las dependencias están instaladas.

## Tarea 3 — Yamil — M2: FastAPI, Pydantic y endpoints de salud

- Crear `backend/main.py`: app FastAPI y router de la API.
- Crear `backend/api/schemas.py`: esquemas Pydantic (SessionState, PersonProfile).
- Implementar `GET /api/status` y `GET /api/camera/status`.
- Iniciar el backend y verificar las respuestas de los endpoints.

**Criterio de aceptación:** el backend arranca y devuelve las respuestas de los endpoints de salud.

## Tarea 4 — Rafael — M2: Repositorio de perfiles

- Crear `backend/database/repository.py`: carga de `profiles.json`, validación del campo `consent`, `get_profile(id)`.
- Crear `backend/database/profiles.json` con datos ficticios.

**Criterio de aceptación:** el repositorio carga el JSON y devuelve perfiles públicos válidos.

## Tarea 5 — Said — M2: Endpoints de sesión

- Implementar `GET /api/session` (estados: waiting, processing, recognized, unknown, error).
- Implementar `POST /api/session/reset` (vuelve a waiting).
- Verificar con `curl` o `httpx`.

**Criterio de aceptación:** los endpoints devuelven respuestas coherentes.

## Tarea 6 — Diego — M2: Tests del repositorio y endpoints

- Crear `tests/test_database.py` (carga de perfiles, consent, perfiles públicos).
- Ampliar `tests/test_api.py` con smoke tests de `/api/status` y `/api/session`.
- Ejecutar `pytest`.

**Criterio de aceptación:** todos los tests pasan.

## Tarea 7 — Yamil — M3: Inicialización de Flet y pantallas

- Crear `frontend/main.py`: app shell de Flet.
- Crear `frontend/screens/welcome.py`, `waiting.py`, `processing.py`, `recognized.py`, `unknown.py` (plantillas).

**Criterio de aceptación:** la app arranca.

## Tarea 8 — Rafael — M3: Pantallas de bienvenida y espera

- Implementar `frontend/screens/welcome.py` y `frontend/screens/waiting.py`.

**Criterio de aceptación:** pantallas visible y funcionales.

## Tarea 9 —Alcides — M3: Pantallas de procesamiento y visitante desconocido

- Implementar `frontend/screens/processing.py` y `frontend/screens/unknown.py`.

**Criterio de aceptación:** pantallas visible y funcionales.

## Tarea 10 — Said — M3: Pantalla de visitante reconocido

- Implementar `frontend/screens/recognized.py`.

**Criterio de aceptación:** pantalla visible y funcional.

## Tarea 11 — Diego — M4: Tarjetas y componentes visuales

- Crear `frontend/components/profile_card.py`, `interest_card.py`, `recommendation_card.py`.
- Mantener consistencia visual básica.

**Criterio de aceptación:** componentes reutilizables.

## Tarea 12 — Yamil — M4: Cliente HTTP y sesión

- Crear `frontend/services/api_client.py` con el cliente HTTPX.
- Implementar polling de sesión: `GET /api/session`.

**Criterio de aceptación:** el cliente consulta el backend periódicamente.

## Tarea 13 — Rafael — M4: Navegación y estados

- Navegación entre pantallas y manejo de estados (cargando, sin conexión, datos recibidos).

**Criterio de aceptación:** la app navega y maneja estados.

## Tarea 14 —Alcides — M4: Reset y recuperación

- Implementar el reset (`POST /api/session/reset`) y el manejo de errores de conexión.

**Criterio de aceptación:** la sesión vuelve a waiting tras la interacción.

## Tarea 15 — Said — M5: Servicio de cámara

- Crear `backend/camera/camera_service.py`: OpenCV (captura, inicio, `get_status()`).

**Criterio de aceptación:** el servicio captura frames y reporta el estado de la cámara.

## Tarea 16 — Diego — M5: Reconocimiento facial

- Crear `backend/recognition/face_service.py`: detección, inscripción con consent, reconocimiento local, validación de confianza, manejo de desconocidos.

**Criterio de aceptación:** solo participantes consensuados y confianza suficiente.

## Tarea 17 — Yamil — M5: Sesión y recomendaciones

- Crear `backend/services/session_service.py` y `backend/services/recommendation.py`.

**Criterio de aceptación:** sesión al identificar y recomendaciones por intereses.

## Tarea 18 — Rafael — M5: Tests de backend

- Ampliar `tests/test_api.py` (estados de sesión completos) y crear `tests/test_recommendations.py`.

**Criterio de aceptación:** tests pasan.

## Tarea 19 —Alcides — M6: Integración final

- Arrancar backend + frontend; verificación E2E; configuración Wi-Fi local (`API_BASE_URL`).

**Criterio de aceptación:** flujo completo funciona.

## Tarea 20 — Said — M6: Documentación

- Crear `docs/architecture.md`, `docs/api_contract.md`, `docs/installation.md`, `docs/team_workflow.md`; actualizar `README.md`.

**Criterio de aceptación:** documentación completa.

## Tarea 21 — Diego — M6: Verificación y cierre

- Ejecutar todos los tests y revisar los criterios de aceptación; ajustes finales.

**Criterio de aceptación:** MVP verificado.
