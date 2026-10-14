import re
from app.models.policy_models import CoverageItem
from datetime import datetime


def extract_total_premium(text: str) -> float | None:
    match = re.search(r"total\s+premium\s*:\s*\$?([\d,]+(?:\.\d{2})?)", text, re.IGNORECASE)
    if not match:
        return None

    amount_str = match.group(1).replace(",", "")
    return float(amount_str)



def extract_term_months_from_policy_period(policy_period: str | None) -> int | None:
    if not policy_period:
        return None

    match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})\s*(?:to|-|through)\s*(\d{1,2}/\d{1,2}/\d{2,4})", policy_period, re.IGNORECASE)
    if not match:
        return None

    start = datetime.strptime(match.group(1), "%m/%d/%Y")
    end = datetime.strptime(match.group(2), "%m/%d/%Y")

    months = (end.year - start.year) * 12 + (end.month - start.month)
    if months <= 0:
        return None

    return months

def extract_policy_term_months(text: str) -> int | None:
    match = re.search(r"term\s*:\s*(\d+)\s*month(?:\(s\)|s)?", text, re.IGNORECASE)
    if not match:
        return None
def extract_deductible(text: str, coverage_name: str) -> int | None:
    pattern = rf"{coverage_name}[^\n]{{0,120}}deductible[^\n]{{0,80}}\$([\d,]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None

    amount_str = match.group(1).replace(",", "")
    value = int(amount_str)

    if value <= 0:
        return None

    if value > 20000:
        return None

    return value

def extract_policy_term_months(text: str) -> int | None:
    match = re.search(r"term\s*:\s*(\d+)\s*month(?:\(s\)|s)?", text, re.IGNORECASE)
    if not match:
        return None

        return int(match.group(1))

    return int(match.group(1))

def extract_policy_period(text: str) -> str | None:
    match = re.search(
        r"policy\s*period\s*:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}\s*(?:to|-|through)\s*[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None

    return match.group(1).strip()

def extract_with_keywords(text: str, keywords: list[str]) -> int | None:
    for keyword in keywords:
        value = extract_deductible(text, keyword)
        if value is not None:
            return value
    return None

def build_coverage_item(text: str, display_name: str, keyword: str) -> CoverageItem:
    deductible = extract_deductible(text, keyword)
    return CoverageItem(name=display_name, deductible=deductible)

