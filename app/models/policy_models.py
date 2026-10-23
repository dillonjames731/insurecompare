from pydantic import BaseModel


class CoverageItem(BaseModel):
    name: str
    limit: str | None = None
    deductible: float | None = None


class PolicySummary(BaseModel):
    bodily_injury_limit: str | None = None
    property_damage_limit: str | None = None
    uninsured_motorist_limit: str | None = None
    pip_limit: str | None = None
    medical_payments_limit: str | None = None
    has_rental: bool | None = None
    has_towing: bool | None = None
    total_premium: float | None = None
    term_months: int | None = None
    policy_period: str | None = None
    collision_deductible: float | None = None
    comprehensive_deductible: float | None = None
