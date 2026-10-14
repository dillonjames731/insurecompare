from pydantic import BaseModel

class CoverageItem(BaseModel):
    name: str
    limit: str | None = None
    deductible: int | None = None