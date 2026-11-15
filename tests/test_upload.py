from fastapi.testclient import TestClient
from app.main import app
from app.api import upload
from app.models.policy_models import PolicySummary
from app.services import document_service

client = TestClient(app)


def fake_extract_text(pdf_bytes):
    return pdf_bytes.decode()


def fake_analyze(text, use_ai):
    if "dec" in text:
        return PolicySummary(total_premium=1073, term_months=6, has_rental=True), {}
    return PolicySummary(total_premium=2050, term_months=12, has_rental=True), {}


def test_analyze_rejects_non_pdf():
    response = client.post("/compare/analyze", files={
        "dec_page": ("notes.txt", b"hello", "text/plain"),
        "quote_page": ("quote.pdf", b"fake pdf", "application/pdf"),
    })
    assert response.status_code == 400


def test_full_compare_flow(monkeypatch):
    monkeypatch.setattr(upload, "extract_text_from_pdf", fake_extract_text)
    monkeypatch.setattr(upload, "analyze_document", fake_analyze)

    response = client.post("/compare/analyze", files={
        "dec_page": ("dec.pdf", b"dec pdf", "application/pdf"),
        "quote_page": ("quote.pdf", b"quote pdf", "application/pdf"),
    })
    report = response.json()
    assert response.status_code == 200
    assert report["overall_summary"].startswith("The new quote is $8.00 cheaper per month.")
    assert report["comparisons"]["add_ons"]["rental"]["summary"] == "Both quotes include rental."

def test_rejects_files_over_the_size_limit(monkeypatch):
    monkeypatch.setattr(upload, "MAX_FILE_BYTES", 10)
    response = client.post("/compare/analyze", files={
        "dec_page": ("dec.pdf", b"x" * 11, "application/pdf"),
        "quote_page": ("quote.pdf", b"small", "application/pdf"),
    })
    assert response.status_code == 413

def test_ai_checkbox_value_reaches_the_analyzer(monkeypatch):
    seen = []

    def spy_analyze(text, use_ai):
        seen.append(use_ai)
        return fake_analyze(text, use_ai)

    monkeypatch.setattr(upload, "extract_text_from_pdf", fake_extract_text)
    monkeypatch.setattr(upload, "analyze_document", spy_analyze)
    client.post("/compare/analyze", data={"use_ai": "false"}, files={
        "dec_page": ("dec.pdf", b"dec pdf", "application/pdf"),
        "quote_page": ("quote.pdf", b"quote pdf", "application/pdf"),
    })
    assert seen == [False, False]

def ai_must_not_run(text):
    raise AssertionError("the AI was called even though use_ai was False")


def test_ai_is_skipped_when_disabled(monkeypatch):
    monkeypatch.setattr(document_service, "extract_with_ai", ai_must_not_run)
    summary, sources = document_service.analyze_document("Total Premium: $2,050.00", use_ai=False)
    assert sources["collision_deductible"] == "not_found"
