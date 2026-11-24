# Contrato de la API — FACEBOT

Contrato implementado en `backend/api/routes.py` (§7).

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

Perfil público de un participante inscrito (§8). Respuesta 404 si el id no existe o el participante no dio consent.

## POST /api/session/reset

Vuelve a `waiting` (§7, §10 regla 10).

## POST /api/recognition/scan

Desencadena un ciclo de reconocimacial sobre demanda (§2 obj. 3). Devuelve el estado de la sesión tras el escaneo (§7).

Sin cámara disponible: respuesta `200` con `{"status":"waiting","person":null}` — el escaneo está controlado (§10).

## POST /api/recognition/enroll/{id}

Inscribe la plantilla de un rostro de un participante consensuado (§5, §10).

Solicitud: `{"image_base64": "<base64 de la imagen>"}`.

Respuesta:

```json
{
  "status": "enrolled",
  "profile_id": "USR001",
  "template_count": 1
}
```

Respuesta 404 si el participante no existe o no dio consent (§10).

## Endpoints adicionales

Todo endpoint adicional se documenta aquí antes de implementarlo (§7).
