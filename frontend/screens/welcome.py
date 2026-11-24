"""Bienvenida al asistente de la feria universitaria."""

from collections.abc import Callable

import flet as ft


class WelcomeScreen(ft.Column):
    """Presenta FACEBOT y permite iniciar una interacción."""

    def __init__(self, on_start: Callable[[ft.Event[ft.Button]], None]) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            tight=True,
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.FACE, size=36, color="#6DE8D1"),
                    alignment=ft.Alignment.CENTER,
                    width=72,
                    height=72,
                    bgcolor="#1B3944",
                    border_radius=24,
                ),
                ft.Text("FACEBOT", size=15, weight=ft.FontWeight.BOLD, color="#6DE8D1"),
                ft.Text(
                    "Bienvenido a la feria",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Descubre proyectos universitarios según tus intereses.",
                    size=17,
                    color="#BAC9DB",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Button(
                    "Comenzar",
                    icon=ft.Icons.ARROW_FORWARD,
                    height=48,
                    bgcolor="#6DE8D1",
                    color="#10222B",
                    on_click=on_start,
                ),
            ],
        )
