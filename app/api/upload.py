import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.services.cleanup_service import normalize_text
from app.services.compare_service import compare_deductibles
from app.services.compare_service import compare_policy_period
from app.services.compare_service import compare_premiums, compare_terms
from app.services.document_service import analyze_document
from app.services.extraction_service import extract_text_from_pdf

router = APIRouter(prefix="/compare", tags=["compare"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _validate_pdf(upload: UploadFile) -> None:
    if not upload.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    if not upload.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"{upload.filename} is not a PDF")


@router.post("/upload")
async def upload_documents(
        dec_page: UploadFile = File(...),
        quote: UploadFile = File(...),
):
    _validate_pdf(dec_page)
    _validate_pdf(quote)
    comparison_id = f"{uuid.uuid4()}"
    dec_name = f"{comparison_id}_dec.pdf"
    quote_name = f"{comparison_id}_quote.pdf"

    dec_path = os.path.join(UPLOAD_DIR, dec_name)
    quote_path = os.path.join(UPLOAD_DIR, quote_name)

    dec_bytes = await dec_page.read()
    quote_bytes = await quote.read()

    with open(dec_path, "wb") as f:
        f.write(dec_bytes)
    with open(quote_path, "wb") as f:
        f.write(quote_bytes)

    return {
        "comparison_id": comparison_id,
        "files": {
            "dec_page": dec_name,
            "quote": quote_name,
        },
        "message": "File uploaded successfully",
    }


class ExtractRequest(BaseModel):
    comparison_id: str


@router.post("/extract")
def extract_documents(payload: ExtractRequest):
    dec_path = os.path.join(UPLOAD_DIR, f"{payload.comparison_id}_dec.pdf")
    quote_path = os.path.join(UPLOAD_DIR, f"{payload.comparison_id}_quote.pdf")

    if not os.path.exists(dec_path) or not os.path.exists(quote_path):
        raise HTTPException(status_code=400, detail="files not found for this comparison_id")

    dec_text = normalize_text(extract_text_from_pdf(dec_path))
    quote_text = normalize_text(extract_text_from_pdf(quote_path))
    current, current_services = analyze_document(dec_text)
    quote, quote_services = analyze_document(quote_text)

    premium_comparison = compare_premiums(current.total_premium, quote.total_premium)
    term_comparison = compare_terms(current.term_months, quote.term_months)
    policy_period_comparison = compare_policy_period(current.policy_period, quote.policy_period)
    collision_deductible_comparison = compare_deductibles(current.collision_deductible, quote.collision_deductible,
                                                          "collision")
    comprehensive_deductible_comparison = compare_deductibles(current.comprehensive_deductible,
                                                              quote.comprehensive_deductible, "comprehensive")
    overall_summary = f"{premium_comparison['summary']} {term_comparison['summary']}"

    return {
        "comparison_id": payload.comparison_id,
        "current": current.model_dump(),
        "quote": quote.model_dump(),
        "sources": {
            "current": current_services,
            "quote": quote_services,
        },
        "comparisons": {
            "premium": premium_comparison,
            "term": term_comparison,
            "policy_period": policy_period_comparison,
            "deductibles": {
                "collision": collision_deductible_comparison,
                "comprehensive": comprehensive_deductible_comparison
            }
        },

        "overall_summary": overall_summary,
    }
