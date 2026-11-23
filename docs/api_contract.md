# Contrato de la API — FACEBOT

Contrato implementado en `backend/api/routes.py` (S7).

## GET /api/status

Disponibilidad del backend.

Ejemplo de respuesta:

```json
{
  "status": "online",
  "application": "FACEBOT"
}
```

## GET /api/camera/status

Estado de la cámara.

Ejemplo:

```json
{
  "status": "connected",
  "camera_available": true
}
```

## GET /api/session

Estado de la sesión. Estados posibles: `waiting`, `processing`, `recognized`, `unknown`, `error`.

Ejemplo waiting:

```json
{
  "status": "waiting",
  "person": null
}
```

Ejemplo recognized:

```json
{
  "status": "recognized",
  "person": {
    "id": "USR001",
    "name": "Carlos",
    "career": "Ingenieria de Sistemas",
    "interests": ["Inteligencia Artificial", "Robotica"],
    "recommendations": [
      {
        "title": "Proyecto de IA",
        "description": "Proyecto universitario de inteligencia artificial",
        "category": "Inteligencia Artificial"
      }
    ]
  }
}
```

Ejemplo unknown:

```json
{
  "status": "unknown",
  "person": null
}
```

## GET /api/person/{id}

Perfil público de un participante inscrito (S8). Respuesta 404 si el id no existe o el participante no dio consent.

## POST /api/session/reset

Vuelve a `waiting` (S7, S10 regla 10).

## Endpoints adicionales

Todo endpoint adicional se documenta aquí antes de implementarlo (S7).
