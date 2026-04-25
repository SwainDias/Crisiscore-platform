"""
app/schemas/guest/checkin.py
"""

from pydantic import BaseModel

from app.core.constants import BloodType, MobilityNeed


class PrefillRoom(BaseModel):
    room_id: str
    room_number: str
    wing: str
    floor: int


class ExistingEmergencyProfile(BaseModel):
    blood_type: BloodType | None = None
    mobility_needs: list[MobilityNeed] = []
    medical_notes: str | None = None


class GuestCheckinPrefillResponse(BaseModel):
    guest_id: str
    room: PrefillRoom
    existing_profile: ExistingEmergencyProfile


class EmergencyProfileInput(BaseModel):
    blood_type: BloodType | None = None
    mobility_needs: list[MobilityNeed] = []
    medical_notes: str | None = None
    share_with_responders: bool


class GuestCheckinSubmitRequest(BaseModel):
    guest_id: str
    room_id: str
    emergency_profile: EmergencyProfileInput


class GuestCheckinSubmitResponse(BaseModel):
    success: bool
    checkin_id: str
    next_route: str
