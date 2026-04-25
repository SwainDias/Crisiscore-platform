"""
app/schemas/staff/safety_check.py
"""

from pydantic import BaseModel

from app.core.constants import ConnectivityStatus, DeviceHealth, ShiftStatus


class Zone(BaseModel):
    zone_id: str
    label: str
    sector: str
    route: str


class ShiftStatusInfo(BaseModel):
    status: ShiftStatus
    started_at: str
    elapsed_seconds: int


class DeviceStatusInfo(BaseModel):
    health: DeviceHealth
    battery_percent: int
    connectivity: ConnectivityStatus


class SafetyCheckResponse(BaseModel):
    check_id: str
    employee_id: str
    generated_at: str
    current_zone: Zone
    shift_status: ShiftStatusInfo
    device_status: DeviceStatusInfo


class SafetyCheckConfirmRequest(BaseModel):
    check_id: str
    employee_id: str
    confirmed_at: str
    override_note: str | None = None


class SafetyCheckConfirmResponse(BaseModel):
    success: bool
    next_check_at: str
