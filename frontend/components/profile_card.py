"""Tarjeta de perfil (§7, M3 - Ashly)."""

from typing import Any, Dict

import flet as ft


class ProfileCard(ft.Container):
    """Muestra el perfil público del participante (§7, §2 obj. 9)."""

    def __init__(self, profile: Dict[str, Any]) -> None:
        super().__init__(
            width=460,
            padding=24,
            bgcolor="#1B3944",
            border_radius=20,
            border=ft.Border.all(1, "#2B4057"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Text(
                        str(profile.get("name", "")),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#6DE8D1",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(profile.get("career", "")),
                        size=16,
                        color="#BAC9DB",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )
