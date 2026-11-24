"""Pantalla de visitante desconocido: interacción manual (§2 obj. 10, §10)."""

from typing import Any, Callable, Dict, Optional

import flet as ft


class UnknownScreen(ft.Column):
    """Informa que la visita no se identificó y ofrece interacción manual (§2 obj. 10)."""

    def __init__(self, on_back: Callable, profile: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            tight=True,
            controls=[
                ft.Icon(ft.Icons.PERSON_OFF, size=48, color="#6DE8D1"),
                ft.Text(
                    "Visita no identificada",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color="#6DE8D1",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "No pudimos identificarte. Navega por el hall de exposiciones "
                    "o contacta a un organizador.",
                    size=16,
                    color="#BAC9DB",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Button(
                    "Volver al inicio",
                    icon=ft.Icons.ARROW_BACK,
                    height=48,
                    color="#6DE8D1",
                    on_click=on_back,
                ),
            ],
        )
