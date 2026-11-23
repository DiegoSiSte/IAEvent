"""Lógica de recomendaciones: proyectos universitarios por interés (S2 obj. 7, S8)."""

import unicodedata
from typing import List, Optional


def _normalize(text: str) -> str:
    """Normaliza un texto: sin acentos, minúsculas, sin espacios extra."""
    decomposed = unicodedata.normalize("NFKD", str(text).lower().strip())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


_CATALOGO = [
    {
        "title": "Proyecto de IA",
        "description": "Desarrollo de una solución de inteligencia artificial",
        "category": "Inteligencia Artificial",
    },
    {
        "title": "Robótica Educativa",
        "description": "Prototipo de robot para laboratorios universitarios",
        "category": "Robótica",
    },
    {
        "title": "Videojuegos Educativos",
        "description": "Desarrollo de juegos educativos para estudiantes",
        "category": "Videojuegos",
    },
    {
        "title": "Diseño de productos",
        "description": "Proyecto de diseño industrial con impacto real",
        "category": "Diseño de productos",
    },
    {
        "title": "Jardinería urbana",
        "description": "Proyecto de jardinería en espacios universitarios",
        "category": "Jardinería",
    },
    {
        "title": "Ciencia ciudadana",
        "description": "Monitoreo ambiental con la comunidad local",
        "category": "Biología ambiental",
    },
]


def build_recommendations(interests: Optional[List[str]] = None, max_items: int = 3) -> List[dict]:
    """Recomendaciones ficticias cuya categoría coincide con un interés del participante."""
    wanted = {_normalize(interest) for interest in (interests or [])}
    wanted.discard("")
    if not wanted:
        return []
    recomendaciones: List[dict] = []
    for item in _CATALOGO:
        categoria = _normalize(item["category"])
        if any(interest in categoria for interest in wanted):
            recomendaciones.append(dict(item))
            if len(recomendaciones) >= max_items:
                break
    return recomendaciones
