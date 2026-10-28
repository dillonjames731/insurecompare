from app.services.compare_service import monthly_cost, compare_monthly_cost
from app.services.compare_service import monthly_cost, compare_monthly_cost, limit_to_numbers, compare_limits, compare_add_on

def test_monthly_cost_divides_and_rounds():
    assert monthly_cost(1073, 6) == 178.83

def test_monthly_cost_missing_premium_returns_none():
    assert monthly_cost(None, 6) is None

def test_monthly_cost_zero_months_returns_none():
    assert monthly_cost(500, 0) is None

def test_compare_monthly_cost_new_is_cheaper():
    result = compare_monthly_cost(178.83, 170.83)
    assert result["difference"] == -8.0
    assert result["summary"] == "The new quote is $8.00 cheaper per month."

def test_compare_monthly_cost_new_is_more_expensive():
    result = compare_monthly_cost(170.83, 178.83)
    assert result["summary"] == "The new quote is $8.00 more expensive per month."

def test_compare_monthly_cost_missing_detail():
    result= compare_monthly_cost(None, 170.83)
    assert result["status"] == "insufficient_data"

def test_limit_to_numbers_split_limit():
    assert limit_to_numbers("$50,000 / $100,000") == [50000.0, 100000.0]

def test_limit_to_numbers_no_dollar_amounts():
    assert limit_to_numbers("Not included") == []


def test_compare_limits_new_is_higher():
    result = compare_limits("$50,000 / $100,000", "$100,000 / $300,000", "bodily injury")
    assert result["summary"] == "The new quote has higher bodily injury limits ($100,000 / $300,000 vs $50,000 / $100,000)."


def test_compare_limits_missing_new_side():
    result = compare_limits("$50,000", None, "pip")
    assert result["status"] == "insufficient_data"


def test_compare_add_on_drops():
    result = compare_add_on(True, False, "rental")
    assert result["summary"] == "The new quote drops rental."


def test_compare_add_on_both_include():
    result = compare_add_on(True, True, "towing")
    assert result["summary"] == "Both quotes include towing."


def test_compare_add_on_false_is_not_missing():                 # 🌑 off ≠ broken
    result = compare_add_on(False, False, "towing")
    assert result["status"] == "ok"

