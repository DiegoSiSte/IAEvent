"""Tarjeta de recomendación (§7, §8, M3 - Ashly)."""

import flet as ft


class RecommendationCard(ft.Container):
    """Muestra una recomendación de proyecto universitario (§7)."""

    def __init__(self, title: str, description: str, category: str) -> None:
        super().__init__(
            padding=16,
            bgcolor="#142234",
            border_radius=16,
            border=ft.Border.all(1, "#2B4057"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=4,
                controls=[
                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color="#6DE8D1"),
                    ft.Text(description, size=13, color="#BAC9DB"),
                    ft.Text(f"Categoría: {category}", size=12, color="#6DE8D1"),
                ],
            ),
        )
