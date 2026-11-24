"""FACEBOT backend — FastAPI application entry point (§2 objectives, §4 architecture).

M5 (Diego): ciclo de reconocimacial en segundo plano: GET /api/session refleja
el estado: waiting / processing / recognized / unknown / error.
"""

import os
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api import routes
from backend.services.session_service import SessionService, recognition_cycle

camera_service = routes.camera_service
face_service = routes.face_service
repository = routes.repository
session_service = routes.session_service
CYCLE_INTERVAL = float(os.getenv("RECOGNITION_INTERVAL", "1.5"))


def _recognition_loop() -> None:
    """Ciclo continuo: reconoce rostros y actualiza la sesión visible."""
    while True:
        try:
            recognition_cycle(camera_service, face_service, repository, session_service)
        except Exception:
            session_service.set(SessionService.ERROR)
        time.sleep(CYCLE_INTERVAL)


def start_recognition_loop() -> None:
    """Arranca el ciclo de reconocimacial en un hilo daemon."""
    thread = threading.Thread(target=_recognition_loop, name="facebot-recognition", daemon=True)
    thread.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_recognition_loop()
    yield


app = FastAPI(
    title="FACEBOT",
    description="Universidad - Proyecto de ingeniería de software (IAEvent).",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(routes.router)
