"""Tests del repositorio: base JSON, consent, perfiles públicos (S8, S10)."""

from backend.database.repository import ProfileRepository


def test_repository_loads_base_json():
    repository = ProfileRepository()
    assert repository.get_profile("USR001") is not None


def test_consented_participant_is_identified():
    repository = ProfileRepository()
    profile = repository.get_profile("USR001")
    assert profile is not None
    assert profile["name"] == "Carlos"


def test_non_consented_participant_is_not_identified():
    repository = ProfileRepository()
    assert repository.get_profile("USR003") is None


def test_unknown_participant_is_not_identified():
    repository = ProfileRepository()
    assert repository.get_profile("USR999") is None


def test_public_profile_has_no_internal_fields():
    repository = ProfileRepository()
    profile = repository.get_profile("USR001")
    assert profile is not None
    assert set(profile.keys()) == {"id", "name", "career", "interests", "recommendations"}
