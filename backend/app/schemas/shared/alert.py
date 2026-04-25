"""
app/schemas/shared/alert.py
"""

from pydantic import BaseModel

from app.core.constants import AlertUserType, IncidentSeverity
from app.schemas.shared.base import LocationSchema


class AlertTypeItem(BaseModel):
    type_id: str
    label: str
    description: str
    icon: str
    color_hex: str
    severity_default: IncidentSeverity


class AlertTypesResponse(BaseModel):
    types: list[AlertTypeItem]


class RaisedBy(BaseModel):
    user_type: AlertUserType
    user_id: str


class RaiseAlertRequest(BaseModel):
    type_id: str
    additional_details: str | None = None
    location: LocationSchema
    raised_by: RaisedBy
    device_id: str
    timestamp: str


class RaiseAlertResponse(BaseModel):
    success: bool = True
    alert_id: str
    incident_id: str | None = None
    message: str
    responders_notified: int
    next_route: str


class AlertErrorResponse(BaseModel):
    success: bool = False
    code: str
    message: str
