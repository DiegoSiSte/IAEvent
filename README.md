# FACEBOT — Universidad (proyecto IAEVENT)

Asistente inteligente que usa cámara y reconocimiento facial para identificar participantes previamente inscritos y consensuados. Tras la identificación muestra información personalizada: perfil, intereses y recomendaciones de proyectos universitarios.

## Arquitectura

Cliente-servidor modular (S4): [docs/architecture.md](docs/architecture.md).

- Backend: FastAPI (S4), repositorio JSON (S8), sesión (S7), recomendaciones (S2 obj. 7).
- Frontend: Flet (S4).
- Frontend integrado con el backend y flujo de reconocimiento operativo.
 - Reconocimiento facial local con OpenCV LBPH, plantillas separadas y consentimiento.

## Estructura

Ver [S5 del documento AGENTS.md](AGENTS.md#5-official-project-structure).

## Equipo

Según [S6 del documento AGENTS.md](AGENTS.md#6-team-responsibilities):

- **Ashly** — diseño visual y UX: `frontend/screens/`, `frontend/components/`.
- **Rafael** — lógica del frontend y API: `frontend/main.py`, `frontend/services/`.
- **Yamil** — backend, computación visual y integración: `backend/`, `tests/`, `docs/`.

Orden y responsables por tarea: [TAREAS.md](TAREAS.md).

## Instalación

Ver [docs/installation.md](docs/installation.md).

## Base funcional

- Backend: endpoints `GET /api/status`, `GET /api/camera/status`, `GET /api/session`, `GET /api/person/{id}`, `POST /api/session/reset` (S7; contrato: [docs/api_contract.md](docs/api_contract.md)).
- Tests iniciales: `pytest` (S15; ver [docs/installation.md](docs/installation.md)).
