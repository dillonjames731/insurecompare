from app.models.policy_models import PolicySummary
from app.services import document_service

def fake_ai(text):
    return PolicySummary(collision_deductible=1000.0, total_premium=999.0)


def fake_ai_refuses(text):
    return None


def test_ai_fills_gap_regex_missed(monkeypatch):

    monkeypatch.setattr(document_service, "extract_with_ai", fake_ai)

    summary, sources = document_service.analyze_document("Total Premium: $2,050.00")

    assert summary.collision_deductible == 1000.0

    assert sources["collision_deductible"] == "ai"

def test_regex_wins_when_both_find_value(monkeypatch):

    monkeypatch.setattr(document_service, "extract_with_ai", fake_ai)

    summary, sources = document_service.analyze_document("Total Premium: $2,050.00")

    assert summary.total_premium == 2050.0
    assert sources["total_premium"] == "regex"

def test_not_found_when_ai_returns_none(monkeypatch):
    monkeypatch.setattr(document_service, "extract_with_ai", fake_ai_refuses)
    summary, sources = document_service.analyze_document("Total Premium: $2,050.00")
    assert summary.collision_deductible is None
    assert sources["collision_deductible"] == "not_found"




