# TAREAS — FACEBOT (proyecto IAEVENT)

> **Regla de orden:** las tareas faltantes siguen un orden secuencial. Cuando una persona termina su tarea, la siguiente en la lista puede iniciar; **no hay tareas en paralelos**.

## Equipo

1. Said
2. Diego
3. Yamil
4. Rafael
5. Alcides

---

## Estado verificado (revisión reciente)

- **Estructura:** verificada contra la estructura oficial de AGENTS.md (S5): todos los archivos presentes (raíz: `AGENTS.md`, `TAREAS.md`, `README.md`, `requirements.txt`, `.gitignore`, `.env.example`; `backend/`: `main.py`, `api/{routes.py, schemas.py}`, `camera/camera_service.py`, `recognition/face_service.py`, `database/{repository.py, profiles.json}`, `services/{recommendation.py, session_service.py}`; `frontend/`: `main.py`, `screens/{welcome, waiting, processing, recognized, unknown}.py`, `components/{profile_card, interest_card, recommendation_card}.py`, `services/api_client.py`; `tests/`: `test_api.py`, `test_database.py`, `test_recommendations.py`; `docs/`: `architecture.md`, `api_contract.md`, `installation.md`, `team_workflow.md`).
- **Pruebas:** `pytest` re-ejecutado: **15 passed, 1 warning** (StarletteDeprecationWarning de httpx en TestClient).
- **Git:** estado limpio (`## main...origin/main`); HEAD = `d4a388f`; `ls-remote` → `refs/heads/main = d4a388fda975fadddb5f2d9f0a8e954f42381b60`.
- **Endpoints (verificados en vivo):** `GET /api/status` → `{"status":"online","application":"FACEBOT"}`; `GET /api/session` → `{"status":"waiting","person":null}`; `GET /api/camera/status` → `{"status":"disconnected","camera_available":false}`; `GET /api/person/USR001` → perfil de Carlos; `POST /api/session/reset` → `{"status":"waiting","person":null}`.

**A todo momento, a quién le toca primero: Rafael (T13 — M4: Navegación y estados del frontend).**

---

## Tareas completadas (base funcional creada)

| Tarea | Persona | Milestone | Estado |
|-------|---------|-----------|--------|
| T1 | Said | M1: Estructura del proyecto | Hecho |
| T2 | Diego | M1: Entorno de desarrollo y dependencias | Hecho |
| T3 | Yamil | M2: FastAPI, Pydantic y endpoints de salud | Hecho (verificado en vivo) |
| T4 | Rafael | M2: Repositorio de perfiles | Hecho |
| T5 | Said | M2: Endpoints de sesión | Hecho (verificado en vivo) |
| T6 | Diego | M2: Tests del repositorio y endpoints | Hecho (`pytest`: 15 passed) |
| T7 | Yamil | M3: Inicialización de Flet y pantallas skeleton | Esqueleto |
| T8 | Rafael | M3: Pantallas de bienvenida y espera (skeletons) | Esqueleto |
| T9 | Alcides | M3: Pantallas de procesamiento y visitante desconocido (skeletons) | Esqueleto |
| T10 | Said | M3: Pantalla de visitante reconocido (skeleton) | Esqueleto |
| T11 | Diego | M4: Tarjetas y componentes visuales (skeletons) | Esqueleto |
| T12 | Yamil | M4: Cliente HTTP (`api_client.py`) | Parcial (sin polling real) |
| T15 | Said | M5: Servicio de cámara (`get_status()` funcional) | Parcial (sin captura de frames) |
| T17 | Yamil | M5: Sesión y recomendaciones (`session_service.py`, `recommendation.py`) | Parcial (sin integración) |
| T20 | Said | M6: Documentación (`docs/*.md`) | Hecho |
| T21 | Diego | M6: Verificación y cierre (`pytest`: 15 passed) | Hecho |

---

## Tareas faltantes — orden de ejecución

1. **Rafael — T13 — M4: Navegación y estados del frontend**
   Navegación entre pantallas (`welcome` → `waiting` → `processing` / `recognized` / `unknown`) y manejo de estados (cargando, sin conexión, datos recibidos).
   **Criterio:** la app navega y maneja estados.

2. **Alcides — T14 — M4: Reset y recuperación de la sesión**
   Reset (`POST /api/session/reset`) y manejo de errores de conexión.
   **Criterio:** la sesión vuelve a `waiting` tras la interacción.

3. **Said — T15 — M5: Servicio de cámara — completar**
   Captura de frames, inicio/detención de cámara.
   **Criterio:** el servicio captura frames y reporta estado.

4. **Diego — T16 — M5: Reconocimiento facial**
   Detección, inscripción con consent, reconocimiento local, validación de confianza, manejo de desconocidos.
   **Criterio:** solo participantes consensuados y confianza suficiente.
   *(Nota: por tu instrucción "no desarrolles todavía todo el reconocimiento facial" — esta tarea queda pendiente.)*

5. **Yamil — T17 — M5: Sesión y recomendaciones — integración**
   Integrar `face_service` + `repository` + `session_service`; recomendaciones por intereses en el flujo de reconocimiento.
   **Criterio:** sesión al identificar y recomendaciones por intereses.

6. **Rafael — T18 — M5: Tests de backend**
   Ampliar `tests/test_api.py` (estados de sesión completos) y pruebas de CV.
   **Criterio:** tests pasan.

7. **Alcides — T19 — M6: Integración final**
   Arrancar backend + frontend, verificación E2E, configuración Wi-Fi local (`API_BASE_URL`).
   **Criterio:** flujo completo funciona.
