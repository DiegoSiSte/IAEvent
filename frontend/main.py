"""Punto de entrada del frontend de FACEBOT."""

import flet as ft

from frontend.screens.waiting import WaitingScreen
from frontend.screens.welcome import WelcomeScreen


def main(page: ft.Page) -> None:
    """Muestra el flujo local de bienvenida y espera de M3."""
    page.title = "FACEBOT"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0C1524"
    page.padding = 24

    card = ft.Container(
        width=520,
        padding=32,
        bgcolor="#142234",
        border=ft.Border.all(1, "#2B4057"),
        border_radius=24,
    )

    def show_welcome(event: ft.Event[ft.Button]) -> None:
        card.content = WelcomeScreen(on_start=show_waiting)

    def show_waiting(event: ft.Event[ft.Button]) -> None:
        card.content = WaitingScreen(on_back=show_welcome)

    card.content = WelcomeScreen(on_start=show_waiting)
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


if __name__ == "__main__":
    ft.run(main)
