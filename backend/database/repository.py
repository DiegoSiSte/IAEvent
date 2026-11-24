"""Repositorio de perfiles (S8): base JSON + validación de consent (S10)."""

import json
import os
from pathlib import Path
from threading import RLock
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
        self._lock = RLock()

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
        with self._lock:
            self._load()
            for profile in self._profiles:
                if profile.get("id") == profile_id:
                    if not profile.get("consent"):
                        return None
                    return self._public_profile(profile)
        return None

    def list_ids(self) -> List[str]:
        """IDs de los participantes con consentimiento."""
        with self._lock:
            self._load()
            return [p["id"] for p in self._profiles if p.get("consent")]

    def create_consented_profile(
        self,
        name: str,
        career: str,
        interests: List[str],
    ) -> Dict[str, Any]:
        """Crea un perfil consentido y lo persiste en el JSON."""
        with self._lock:
            self._load()
            existing_ids = {str(profile.get("id", "")) for profile in self._profiles}
            number = 1
            while f"USR{number:03d}" in existing_ids:
                number += 1
            profile = {
                "id": f"USR{number:03d}",
                "name": name.strip(),
                "career": career.strip(),
                "consent": True,
                "interests": [interest.strip() for interest in interests if interest.strip()],
                "recommendations": [],
            }
            self._profiles.append(profile)
            try:
                self._save()
            except OSError:
                self._profiles.pop()
                raise
            return self._public_profile(profile)

    def delete_profile(self, profile_id: str) -> bool:
        """Elimina un perfil; utilizado para revertir una inscripción fallida."""
        with self._lock:
            self._load()
            for index, profile in enumerate(self._profiles):
                if profile.get("id") == profile_id:
                    removed = self._profiles.pop(index)
                    try:
                        self._save()
                    except OSError:
                        self._profiles.insert(index, removed)
                        raise
                    return True
        return False

    def _save(self) -> None:
        temporary_path = self._path.with_name(f".{self._path.name}.tmp")
        try:
            with temporary_path.open("w", encoding="utf-8") as handle:
                json.dump({"profiles": self._profiles}, handle, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self._path)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()

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
