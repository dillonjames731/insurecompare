def monthly_cost(premium: float | None, term_months: int | None) -> float | None:
    if premium is None or term_months is None or term_months == 0:
        return None
    return round(premium / term_months, 2)

def compare_monthly_cost(current_cost: float | None, new_cost: float | None) -> dict:
    if current_cost is None or new_cost is None:
        return {
            "status": "insufficient_data",
            "difference": None,
            "summary": "I could not find monthly cost in one or both documents yet."
        }
    difference = round(new_cost - current_cost, 2)
    if difference < 0:
        summary = f"The new quote is ${abs(difference):,.2f} cheaper per month."
    elif difference > 0:
        summary = f"The new quote is ${abs(difference):,.2f} more expensive per month."
    else:
        summary = "Both quotes have the same monthly cost."

    return {
        "status": "ok",
        "current_cost": current_cost,
        "new_cost": new_cost,
        "difference": difference,
        "summary": summary,

    }





def compare_terms(current_term: int | None, new_term: int | None) -> dict:
    if current_term is None or new_term is None:
        return {
            "status": "insufficient_data",
            "difference": None,
            "summary": "I could not find policy term in one or both documents yet."
        }

    difference = new_term - current_term

    if difference > 0:
        summary = f"The new quote term is {difference} month(s) longer."
    elif difference < 0:
        summary = f"The new quote term is {abs(difference)} month(s) shorter."
    else:
        summary = "Both policy terms are the same length."

    return {
        "status": "ok",
        "difference": difference,
        "summary": summary,
    }
def compare_premiums(current_premium: float | None, new_premium: float | None) -> dict:
    if current_premium is None or new_premium is None:
        return {
            "status": "insufficient_data",
            "difference": None,
            "summary": "I could not find premium in one or both documents yet."
        }

    difference = round(new_premium - current_premium, 2)

    if difference < 0:
        summary = f"The new quote is ${abs(difference):,.2f} cheaper."
    elif difference > 0:
        summary = f"The new quote is ${difference:,.2f} more expensive."
    else:
        summary = "Both premiums are the same."

    return {
        "status": "ok",
        "difference": difference,
        "summary": summary,
    }
def compare_deductibles(current_value: int | None, new_value: int | None, label: str) -> dict:
    if current_value is None or new_value is None:
        return {
            "status": "insufficient_data",
            "difference": None,
            "summary": f"I could not find {label} deductible in one or both documents yet."
        }
    difference = new_value - current_value

    if difference > 0:
        summary = f"The quote you are comparing has a {label} deductible of ${difference:,.0f} more."
    elif difference < 0:
        summary = f"The quote you are comparing has a {label} deductible of ${abs(difference):,.0f} less."
    else:
        summary = f"Both quotes have the same {label} deductible of ${current_value:,.0f}."
    return {
            "status": "ok",
            "difference": difference,
            "summary": summary,
    }

def compare_policy_period(current_period: str | None, new_period: str | None) -> dict:
    if current_period is None or new_period is None:
        return {
            "status": "insufficient_data",
            "difference": None,
            "summary": "I could not find policy period in one or both documents yet."
        }
    if current_period.strip().lower() == new_period.strip().lower():
        return {
            "status": "same",
            "summary": "Both quotes have the same policy period."
        }
    return {
        "status": "different",
        "summary": "The policy period is different between the two documents"
    }

