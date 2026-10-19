from pydantic import BaseModel


class CoverageItem(BaseModel):
    name: str
    limit: str | None = None
    deductible: float | None = None


class PolicySummary(BaseModel):
    total_premium: float | None = None
    term_months: int | None = None
    policy_period: str | None = None
    collision_deductible: float | None = None
    comprehensive_deductible: float | None = None
