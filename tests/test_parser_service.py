from app.services.parser_service import to_number, find_line


def test_to_number_remove_dollar_sign_and_commas():
    assert to_number("$1,865.88") == 1865.88


def test_to_number_without_cents():
    assert to_number("$500") == 500


def test_to_find_line_ignores_capitalization():
    assert find_line("Header\nAuto Collision $500", "COLLISION") == "Auto Collision $500"


def test_to_find_line_returns_none_when_missing():
    assert find_line("Header\nAuto Collision", "towing") is None
