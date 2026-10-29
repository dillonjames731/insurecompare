from fastapi.testclient import TestClient
from app.main import app
from app.api import upload
from app.models.policy_models import PolicySummary

client = TestClient(app)


def fake_extract_text(path):
    return path


def fake_analyze(text):
    if "dec" in text:
        return PolicySummary(total_premium=1073, term_months=6, has_rental=True), {}
    return PolicySummary(total_premium= 2050, term_months= 12, has_rental= True), {}


def test_upload_rejects_non_pdf():
    response = client.post("/compare/upload", files={
        "dec_page": ("notes.txt", b"hello", "text/plain"),
        "quote": ("quote.pdf", b"fake pdf", "application/pdf"),
    })
    assert response.status_code == 400


def test_full_compare_flow(monkeypatch):
    monkeypatch.setattr(upload, "extract_text_from_pdf", fake_extract_text)
    monkeypatch.setattr(upload, "analyze_document", fake_analyze)

    response = client.post("/compare/upload", files={
        "dec_page": ("dec.pdf", b"fake pdf", "application/pdf"),
        "quote": ("quote.pdf", b"fake pdf", "application/pdf"),
    })
    comparison_id = response.json()["comparison_id"]

    response = client.post("/compare/extract", json={"comparison_id": comparison_id})
    report = response.json()
    assert response.status_code == 200
    assert report["overall_summary"].startswith("The new quote is $8.00 cheaper per month.")
    assert report["comparisons"]["add_ons"]["rental"]["summary"] == "Both quotes include rental."

    response = client.post("/compare/extract", json={"comparison_id": comparison_id})
    assert response.status_code == 400