"""FACEBOT backend — FastAPI application entry point (S2 objectives, S4 architecture)."""

from fastapi import FastAPI

from backend.api import routes

app = FastAPI(
    title="FACEBOT",
    description="Universidad - Proyecto de ingeniería de software (IAEvent).",
    version="0.1.0",
)

app.include_router(routes.router)
