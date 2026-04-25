"""
app/schemas/guest/guest.py
Pydantic models for guest/resident endpoints.
"""

from pydantic import BaseModel

from app.core.constants import (
    BloodType,
    GuestAccountabilityStatus,
    GuestAlertType,
    IncidentSeverity,
    InfoHubCategory,
    MobilityNeed,
)


# ─── Guest Home ──────────────────────────────────────────────────────────────

class GuestProfile(BaseModel):
    name: str
    property_name: str
    room_id: str


class ActiveAlertBanner(BaseModel):
    present: bool
    alert_id: str | None = None
    severity: IncidentSeverity | None = None
    title: str | None = None
    body: str | None = None
    cta_label: str | None = None
    cta_route: str | None = None


class QuickAction(BaseModel):
    id: str
    label: str
    description: str
    icon: str
    route: str
    enabled: bool


class InfoHubItem(BaseModel):
    id: str
    category: InfoHubCategory
    title: str
    preview: str
    route: str
    thumbnail_url: str | None = None


class GuestHomeResponse(BaseModel):
    guest: GuestProfile
    active_alert: ActiveAlertBanner
    quick_actions: list[QuickAction]
    info_hub: list[InfoHubItem]
    sos_enabled: bool


# ─── Guest Check-In ───────────────────────────────────────────────────────────

class RoomInfo(BaseModel):
    room_id: str
    room_number: str
    wing: str
    floor: int


class ExistingProfile(BaseModel):
    blood_type: BloodType | None = None
    mobility_needs: list[MobilityNeed] = []
    medical_notes: str | None = None


class CheckinPrefillResponse(BaseModel):
    guest_id: str
    room: RoomInfo
    existing_profile: ExistingProfile


class EmergencyProfile(BaseModel):
    blood_type: BloodType | None = None
    mobility_needs: list[MobilityNeed] = []
    medical_notes: str | None = None
    share_with_responders: bool = True


class CheckinSubmitRequest(BaseModel):
    guest_id: str
    room_id: str
    emergency_profile: EmergencyProfile


class CheckinSubmitResponse(BaseModel):
    success: bool
    checkin_id: str
    next_route: str


# ─── Incident / Alert Guide ───────────────────────────────────────────────────

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
    alert_type: GuestAlertType
    severity: IncidentSeverity
    headline: str
    room_context: RoomContext
    primary_instruction: PrimaryInstruction
    immediate_actions: list[ImmediateAction]
    evacuation_map: EvacuationMap
    last_updated_at: str