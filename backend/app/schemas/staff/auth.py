"""
app/schemas/staff/auth.py
"""

from pydantic import BaseModel, Field

from app.core.constants import StaffRole


# ─── Request ─────────────────────────────────────────────────────────────────

class StaffLoginRequest(BaseModel):
    employee_id: str = Field(..., min_length=1)
    pin: str = Field(..., min_length=4, max_length=8)
    biometric_token: str | None = None
    device_id: str
    property_network_id: str


# ─── Response ────────────────────────────────────────────────────────────────

class StaffProfile(BaseModel):
    employee_id: str
    name: str
    role: StaffRole
    avatar_url: str | None = None
    property_id: str


class PropertyNetworkInfo(BaseModel):
    detected: bool
    property_name: str | None = None
    network_label: str | None = None
    secure_protocol: bool


class StaffLoginResponse(BaseModel):
    success: bool = True
    access_token: str
    refresh_token: str
    expires_in: int
    staff: StaffProfile
    property_network: PropertyNetworkInfo
    biometrics_enabled: bool


# ─── Error ───────────────────────────────────────────────────────────────────

class AuthErrorResponse(BaseModel):
    success: bool = False
    code: str
    message: str
    retry_allowed: bool
