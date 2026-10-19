import re
from app.models.policy_models import CoverageItem, PolicySummary
from datetime import datetime

MONEY_PATTERN = r"\$[\d,]+(?:\.\d{2})?"
PREMIUM_PATTERNS = [r"^total\s+premium:\s*\$", r"^total\s+\$"]


def to_number(amount: str) -> float:
    return float(amount.replace("$", "").replace(",", ""))


def find_line(text: str, keyword: str) -> str | None:
    lines = text.splitlines()
    for line in lines:
        if keyword.lower() in line.lower():
            return line
    return None


def extract_total_premium(text: str) -> float | None:
    lines = text.splitlines()
    for pattern in PREMIUM_PATTERNS:
        for line in lines:
            if re.search(pattern, line.strip(), re.IGNORECASE):
                amounts = re.findall(MONEY_PATTERN, line)
                return to_number(amounts[0])
    return None


def extract_term_months_from_policy_period(policy_period: str | None) -> int | None:
    if not policy_period:
        return None

    match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})\s*(?:to|-|through)\s*(\d{1,2}/\d{1,2}/\d{2,4})", policy_period,
                      re.IGNORECASE)
    if not match:
        return None

    start_raw = match.group(1)
    end_raw = match.group(2)

    def _parse_date(value: str) -> datetime | None:
        for fmt in ["%m/%d/%Y", "%m/%d/%y"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

    start = _parse_date(start_raw)
    end = _parse_date(end_raw)
    if not start or not end:
        return None

    months = (end.year - start.year) * 12 + (end.month - start.month)
    if months <= 0:
        return None

    return months


def extract_deductible(text: str, keyword: str) -> float | None:
    line = find_line(text, keyword)
    if line is None:
        return None
    amounts = re.findall(MONEY_PATTERN, line)
    if len(amounts) < 2:
        return None
    return to_number(amounts[0])


def extract_policy_term_months(text: str) -> int | None:
    match = re.search(r"term\s*:\s*(\d+)\s*month(?:\(s\)|s)?", text, re.IGNORECASE)
    if not match:
        return None
    else:
        return int(match.group(1))


def extract_policy_period(text: str) -> str | None:
    match = re.search(
        r"(?:proposed\s+)?policy\s*period\s*:?\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}\s*(?:to|-|through)\s*[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None

    return match.group(1).strip()


def extract_with_keywords(text: str, keywords: list[str]) -> float | None:
    for keyword in keywords:
        value = extract_deductible(text, keyword)
        if value is not None:
            return value
    return None


def build_coverage_item(text: str, display_name: str, keyword: str) -> CoverageItem:
    deductible = extract_deductible(text, keyword)
    return CoverageItem(name=display_name, deductible=deductible)


def extract_term_from_text_patterns(text: str) -> int | None:
    month_range_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\.?\s*\d*\s*to\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\.?\s*\d*"
    match = re.search(month_range_pattern, text, re.IGNORECASE)
    if not match:
        return None

    start_month = match.group(1).lower()
    end_month = match.group(2).lower()

    month_index = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    start = month_index[start_month]
    end = month_index[end_month]
    diff = (end - start) % 12

    if diff == 0:
        return None

    return diff


def parse_document(text: str) -> PolicySummary:
    policy_period = extract_policy_period(text)
    term_months = extract_policy_term_months(text)
    if term_months is None:
        term_months = extract_term_months_from_policy_period(policy_period)
    if term_months is None:
        term_months = extract_term_from_text_patterns(text)

    return PolicySummary(
        total_premium=extract_total_premium(text),
        term_months=term_months,
        policy_period=policy_period,
        collision_deductible=extract_with_keywords(text, ["collision"]),
        comprehensive_deductible=extract_with_keywords(text, ["comprehensive"]),
    )
