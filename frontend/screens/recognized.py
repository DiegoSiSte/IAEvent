"""Pantalla de visitante reconocido: información personalizada (§7, M3 - Ashly)."""

from typing import Any, Callable, Dict, List

import flet as ft

from frontend.components.interest_card import InterestCard
from frontend.components.profile_card import ProfileCard
from frontend.components.recommendation_card import RecommendationCard


class RecognizedScreen(ft.Column):
    """Muestra el perfil, intereses y recomendaciones del participante (§2 obj. 9)."""

    def __init__(self, on_back: Callable, profile: Dict[str, Any]) -> None:
        interests = [InterestCard(interest=i) for i in profile.get("interests", [])]
        recommendations = [
            RecommendationCard(
                title=r["title"], description=r["description"], category=r["category"]
            )
            for r in profile.get("recommendations", [])
        ]
        controls: List[ft.Control] = [ProfileCard(profile=profile)]
        if interests:
            controls.append(ft.Text("Intereses", size=14, color="#6DE8D1", weight=ft.FontWeight.BOLD))
            controls.extend(interests)
        if recommendations:
            controls.append(
                ft.Text("Recomendaciones", size=14, color="#6DE8D1", weight=ft.FontWeight.BOLD)
            )
            controls.extend(recommendations)
        controls.append(
            ft.Button(
                "Volver al inicio",
                icon=ft.Icons.ARROW_BACK,
                height=48,
                color="#6DE8D1",
                on_click=on_back,
            )
        )
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            controls=controls,
        )
