"""Punto de entrada del frontend de FACEBOT (app shell + navegación, §4).

Navegación (§4 Frontend): Welcome → Waiting → (Processing | Recognized | Unknown).
Session polling: `api_client.get_session()` cada 2s; errores de conexión se
tratan como waiting; reset vuelve a Welcome (§7, §10).
"""

import os
import time
from typing import Any, Dict

import flet as ft

from frontend.screens.processing import ProcessingScreen
from frontend.screens.enrollment import EnrollmentScreen
from frontend.screens.recognized import RecognizedScreen
from frontend.screens.unknown import UnknownScreen
from frontend.screens.waiting import WaitingScreen
from frontend.screens.welcome import WelcomeScreen
from frontend.services.api_client import FacebotApiClient, default_base_url

POLL_INTERVAL = float(os.getenv("FRONTEND_POLL_INTERVAL", "2.0"))


def main(page: ft.Page) -> None:
    """App shell: welcome, waiting, processing y resultados (§4, §2 obj. 9)."""
    page.title = "FACEBOT"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0C1524"
    page.padding = 24

    api = FacebotApiClient(default_base_url())
    picker = ft.FilePicker()
    page.services.append(picker)
    card = ft.Container(
        width=520,
        padding=32,
        bgcolor="#142234",
        border=ft.Border.all(1, "#2B4057"),
        border_radius=24,
    )

    def _show_welcome(event: ft.Event | None = None) -> None:
        card.content = WelcomeScreen(on_start=_show_waiting, on_enroll=_show_enrollment)
        page.update()

    def _show_waiting(event: ft.Event | None = None) -> None:
        card.content = WaitingScreen(on_back=_show_welcome, on_scan=_scan)
        page.update()

    def _show_enrollment(event: ft.Event | None = None) -> None:
        card.content = EnrollmentScreen(picker=picker, api=api, on_back=_show_welcome)
        page.update()

    def _scan(event: ft.Event | None = None) -> None:
        card.content = ProcessingScreen()
        page.update()

        def scan_in_background() -> None:
            try:
                api.scan_recognition()
                session = api.get_session()
            except Exception:
                session = {"status": "error", "person": None}
            _apply_session(session)

        page.run_thread(scan_in_background)

    def _apply_session(session: Dict[str, Any]) -> None:
        """Actualiza la pantalla según el estado de la sesión (§7)."""
        status = session.get("status")
        person = session.get("person")
        if status == "recognized" and person:
            card.content = RecognizedScreen(on_back=_show_welcome, profile=person)
        elif status == "unknown":
            card.content = UnknownScreen(on_back=_show_welcome)
        elif status == "processing":
            card.content = ProcessingScreen()
        elif status == "waiting" and not isinstance(card.content, (WelcomeScreen, EnrollmentScreen)):
            card.content = WaitingScreen(on_back=_show_welcome, on_scan=_scan)
        page.update()

    def _poll() -> None:
        while True:
            try:
                session = api.get_session()
            except Exception:
                # Manejo de errores de conexión (§4 Frontend, §7): treated as waiting.
                session = {"status": "waiting", "person": None}
            _apply_session(session)
            time.sleep(POLL_INTERVAL)

    card.content = WelcomeScreen(on_start=_show_waiting, on_enroll=_show_enrollment)
    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                tight=True,
                controls=[card],
            ),
        )
    )
    page.run_thread(_poll)


if __name__ == "__main__":
    ft.run(main)
