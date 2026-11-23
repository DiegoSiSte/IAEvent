# T3 de Yamil — Verificación en vivo

El 23 de noviembre de 2026 se inició FACEBOT con Uvicorn y se comprobó por HTTP la implementación de FastAPI en `d4a388f`.

| Endpoint | HTTP | Respuesta observada |
| --- | --- | --- |
| `GET /api/status` | 200 | `{"status":"online","application":"FACEBOT"}` |
| `GET /api/camera/status` | 200 | `{"status":"disconnected","camera_available":false}` |

`GET /openapi.json` también devolvió 200 y confirmó los modelos Pydantic `StatusResponse` y `CameraStatusResponse`. El entorno no detectó una cámara, por lo que la prueba cubrió el estado desconectado.

Para reproducir la comprobación, ejecuta `python -m uvicorn backend.main:app` desde la raíz y consulta las rutas anteriores en `http://127.0.0.1:8000`.
