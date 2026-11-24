"""Tarjeta de interés (§8, M3 - Ashly)."""

import flet as ft


class InterestCard(ft.Container):
    """Muestra un interés del participante (§8 DATABASE CONTRACT)."""

    def __init__(self, interest: str) -> None:
        super().__init__(
            padding=ft.Padding.symmetric(horizontal=16, vertical=8),
            bgcolor="#142234",
            border_radius=16,
            border=ft.Border.all(1, "#2B4057"),
            content=ft.Text(interest, size=14, color="#BAC9DB"),
        )
