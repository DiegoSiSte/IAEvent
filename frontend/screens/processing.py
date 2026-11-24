"""Pantalla de procesamiento (M3 - Ashly; base funcional)."""

import flet as ft


class ProcessingScreen(ft.Column):
    """Indica que la identificación está en curso (§2 obj. 4-5)."""

    def __init__(self) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            tight=True,
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=36, color="#6DE8D1"),
                    alignment=ft.Alignment.CENTER,
                    width=72,
                    height=72,
                    bgcolor="#1B3944",
                    border_radius=24,
                ),
                ft.Text(
                    "Procesando",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color="#6DE8D1",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ProgressBar(width=300, height=6, color="#6DE8D1", bgcolor="#1B3944"),
            ],
        )
