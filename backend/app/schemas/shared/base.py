"""
app/schemas/shared/base.py
Shared Pydantic models reused across staff and guest schemas.
"""

from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    lat: float | None = None
    lng: float | None = None
    manual_label: str | None = None


class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    skip: int = Field(default=0, ge=0)


class SuccessResponse(BaseModel):
    success: bool = True
