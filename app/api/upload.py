from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.cleanup_service import normalize_text
from app.services.compare_service import compare_deductibles
from app.services.compare_service import compare_policy_period
from app.services.compare_service import compare_premiums, compare_terms
from app.services.document_service import analyze_document
from app.services.extraction_service import extract_text_from_pdf
from app.services.compare_service import compare_monthly_cost, monthly_cost
from app.services.compare_service import compare_limits, compare_add_on

router = APIRouter(prefix="/compare", tags=["compare"])

MAX_FILE_BYTES = 10 * 1024 * 1024


def _validate_pdf(upload: UploadFile) -> None:
    if not upload.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    if not upload.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"{upload.filename} is not a PDF")


def _build_report(dec_text: str, quote_text: str, use_ai: bool) -> dict:
    current, current_services = analyze_document(dec_text, use_ai)
    quote, quote_services = analyze_document(quote_text, use_ai)
    current_cost = monthly_cost(current.total_premium, current.term_months)
    quote_cost = monthly_cost(quote.total_premium, quote.term_months)

    premium_comparison = compare_premiums(current.total_premium, quote.total_premium)
    term_comparison = compare_terms(current.term_months, quote.term_months)
    policy_period_comparison = compare_policy_period(current.policy_period, quote.policy_period)
    collision_deductible_comparison = compare_deductibles(current.collision_deductible, quote.collision_deductible,
                                                          "collision")
    comprehensive_deductible_comparison = compare_deductibles(current.comprehensive_deductible,
                                                              quote.comprehensive_deductible, "comprehensive")
    monthly_comparison = compare_monthly_cost(current_cost, quote_cost)
    bodily_injury_comparison = compare_limits(current.bodily_injury_limit, quote.bodily_injury_limit, "bodily injury")
    property_damage_comparison = compare_limits(current.property_damage_limit, quote.property_damage_limit,
                                                "property damage")
    uninsured_motorist_comparison = compare_limits(current.uninsured_motorist_limit, quote.uninsured_motorist_limit,
                                                   "uninsured motorist")
    pip_comparison = compare_limits(current.pip_limit, quote.pip_limit, "PIP")
    medical_payments_comparison = compare_limits(current.medical_payments_limit, quote.medical_payments_limit,
                                                 "medical payments")
    rental_comparison = compare_add_on(current.has_rental, quote.has_rental, "rental")
    towing_comparison = compare_add_on(current.has_towing, quote.has_towing, "towing")
    overall_summary = f"{monthly_comparison['summary']} {term_comparison['summary']}"

    return {
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
            "monthly_cost": monthly_comparison,
            "deductibles": {
                "collision": collision_deductible_comparison,
                "comprehensive": comprehensive_deductible_comparison
            },
            "limits": {
                "bodily_injury": bodily_injury_comparison,
                "property_damage": property_damage_comparison,
                "uninsured_motorist": uninsured_motorist_comparison,
                "pip": pip_comparison,
                "medical_payments": medical_payments_comparison,
            },
            "add_ons": {
                "rental": rental_comparison,
                "towing": towing_comparison,
            },
        },

        "overall_summary": overall_summary,
    }


@router.post("/analyze")
async def analyze_documents(
        dec_page: UploadFile = File(...),
        quote_page: UploadFile = File(...),
        use_ai: bool = Form(True)
):
    _validate_pdf(dec_page)
    _validate_pdf(quote_page)
    dec_bytes = await dec_page.read()

    quote_bytes = await quote_page.read()
    if len(dec_bytes) > MAX_FILE_BYTES or len(quote_bytes) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="Each PDF must be 10 MB or smaller")
    dec_text = normalize_text(extract_text_from_pdf(dec_bytes))
    quote_text = normalize_text(extract_text_from_pdf(quote_bytes))
    return _build_report(dec_text, quote_text, use_ai)
