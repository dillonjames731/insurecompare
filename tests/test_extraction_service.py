import anthropic
import httpx
from app.services import ai_extraction_service


def fake_parse_api_down(**kwargs):
    raise anthropic.APIConnectionError(request=httpx.Request("POST", "https://api.anthropic.com"))


def test_returns_none_when_api_is_down(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(ai_extraction_service.client.messages, "parse", fake_parse_api_down)
    assert ai_extraction_service.extract_with_ai("Total Premium: $2,050.00") is None


def test_returns_none_when_key_is_missing(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert ai_extraction_service.extract_with_ai("Total Premium: $2,050.00") is None