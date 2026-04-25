"""
app/schemas/guest/alert.py
"""

from pydantic import BaseModel

from app.core.constants import AlertGuideType, IncidentSeverity


class RoomContext(BaseModel):
    room_id: str
    room_number: str
    is_safe_zone: bool
    safe_zone_note: str | None = None


class PrimaryInstruction(BaseModel):
    title: str
    body: str
    icon: str


class ImmediateAction(BaseModel):
    step: int
    title: str
    body: str


class UserLocation(BaseModel):
    lat: float | None = None
    lng: float | None = None
    label: str | None = None


class EvacuationMap(BaseModel):
    available: bool
    map_url: str | None = None
    user_location: UserLocation


class GuestAlertGuideResponse(BaseModel):
    alert_id: str
    alert_type: AlertGuideType
    severity: IncidentSeverity
    headline: str
    room_context: RoomContext
    primary_instruction: PrimaryInstruction
    immediate_actions: list[ImmediateAction]
    evacuation_map: EvacuationMap
    last_updated_at: str
