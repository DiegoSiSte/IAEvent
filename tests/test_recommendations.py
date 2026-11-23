"""Tests de recomendaciones (S2 obj. 7, S8)."""

from backend.services.recommendation import build_recommendations


def test_recommendations_match_interest():
    recs = build_recommendations(["Inteligencia Artificial"])
    assert any(r["category"] == "Inteligencia Artificial" for r in recs)


def test_recommendations_respect_interests():
    recs = build_recommendations(["Diseño de productos"])
    assert recs
    assert recs[0]["category"] == "Diseño de productos"


def test_no_interests_gives_no_recommendations():
    assert build_recommendations([]) == []
    assert build_recommendations(None) == []
