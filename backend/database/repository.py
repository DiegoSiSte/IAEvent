"""Repositorio de perfiles (S8): base JSON + validación de consent (S10)."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROFILES_PATH = Path(__file__).parent / "profiles.json"


class ProfileRepository:
    """Carga profiles.json y expone perfiles públicos.

    El backend es el único acceso a la base de datos (S4).
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = Path(path) if path is not None else _PROFILES_PATH
        self._profiles: List[Dict[str, Any]] = []
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        with self._path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        self._profiles = data.get("profiles", [])
        for profile in self._profiles:
            profile.setdefault("consent", False)
        self._loaded = True

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Perfil público del participante, o None si no existe / no dio consent."""
        self._load()
        for profile in self._profiles:
            if profile.get("id") == profile_id:
                if not profile.get("consent"):
                    return None
                return self._public_profile(profile)
        return None

    def list_ids(self) -> List[str]:
        """IDs de los participantes con consentimiento."""
        self._load()
        return [p["id"] for p in self._profiles if p.get("consent")]

    @staticmethod
    def _public_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
        """Perfil público: sin datos internos ni biometría (S10)."""
        return {
            "id": profile["id"],
            "name": profile["name"],
            "career": profile["career"],
            "interests": list(profile.get("interests", [])),
            "recommendations": [dict(r) for r in profile.get("recommendations", [])],
        }
