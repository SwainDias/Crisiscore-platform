"""
app/schemas/guest/home.py
"""

from pydantic import BaseModel

from app.core.constants import IncidentSeverity, InfoHubCategory


class GuestSummary(BaseModel):
    name: str
    property_name: str
    room_id: str


class GuestActiveAlert(BaseModel):
    present: bool
    alert_id: str | None = None
    severity: IncidentSeverity | None = None
    title: str | None = None
    body: str | None = None
    cta_label: str | None = None
    cta_route: str | None = None


class QuickActionItem(BaseModel):
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
    guest: GuestSummary
    active_alert: GuestActiveAlert
    quick_actions: list[QuickActionItem]
    info_hub: list[InfoHubItem]
    sos_enabled: bool
