from app.models.policy_models import PolicySummary
from app.services.parser_service import parse_document
from app.services.ai_extraction_service import extract_with_ai


def analyze_document(text: str) -> tuple[PolicySummary, dict]:
    regex_data = parse_document(text).model_dump()

    ai_data = {}
    if None in regex_data.values():
        ai_result = extract_with_ai(text)
        if ai_result is not None:
            ai_data = ai_result.model_dump()

    merged = {}
    sources = {}
    for field, value in regex_data.items():
        if value is not None:
            merged[field] = value
            sources[field] = "regex"
        elif ai_data.get(field) is not None:
            merged[field] = ai_data[field]
            sources[field] = "ai"
        else:
            merged[field] = None
            sources[field] = "not_found"
    return PolicySummary.model_validate(merged), sources