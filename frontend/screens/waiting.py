"""Espera previa al reconocimiento."""

from collections.abc import Callable

import flet as ft


class WaitingScreen(ft.Column):
    """Indica al visitante cómo prepararse y permite volver al inicio."""

    def __init__(self, on_back: Callable[[ft.Event[ft.Button]], None]) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            tight=True,
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.VIDEOCAM_OUTLINED, size=36, color="#6DE8D1"),
                    alignment=ft.Alignment.CENTER,
                    width=72,
                    height=72,
                    bgcolor="#1B3944",
                    border_radius=24,
                ),
                ft.Text("FACEBOT", size=15, weight=ft.FontWeight.BOLD, color="#6DE8D1"),
                ft.Text(
                    "En espera",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Si te inscribiste y autorizaste el reconocimiento, colócate "
                    "frente a la cámara cuando esté disponible.",
                    size=17,
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
