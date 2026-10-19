from app.services.parser_service import to_number, find_line, extract_deductible, extract_total_premium

ALLSTATE_STYLE = """COVERAGE LIMITS DEDUCTIBLE PREMIUM
Automobile Liability Insurance Not Applicable $310.00
Auto Collision Insurance Actual Cash Value $500 $210.00
Auto Comprehensive Insurance Actual Cash Value $250 $85.00
Total Premium
TOTAL $1,240.50
Your total premium reflects a combined discount of $96.00
Total Premium for 05 Compact Car $605.00"""

QUOTE_STYLE = """Quote Prepared For: Sample Customer
Total Premium: $1,865.88
Agent: Sample Agency"""


def test_to_number_remove_dollar_sign_and_commas():
    assert to_number("$1,865.88") == 1865.88


def test_to_number_without_cents():
    assert to_number("$500") == 500


def test_to_find_line_ignores_capitalization():
    assert find_line("Header\nAuto Collision $500", "COLLISION") == "Auto Collision $500"


def test_to_find_line_returns_none_when_missing():
    assert find_line("Header\nAuto Collision", "towing") is None


def test_deductible_collision():
    assert extract_deductible(ALLSTATE_STYLE, "collision") == 500.0


def test_deductible_comprehensive():
    assert extract_deductible(ALLSTATE_STYLE, "comprehensive") == 250.0


def test_deductible_none_when_no_deductible_column():
    assert extract_deductible(ALLSTATE_STYLE, "liability") is None


def test_premium_allstate_style():
    assert extract_total_premium(ALLSTATE_STYLE) == 1240.5


def test_premium_quote_style():
    assert extract_total_premium(QUOTE_STYLE) == 1865.88


def test_premium_none_when_missing():
    assert extract_total_premium("nothing here") is None
