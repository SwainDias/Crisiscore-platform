"""
app/api/v1/guest/checkin.py
GET  /api/v1/guest/checkin/prefill
POST /api/v1/guest/checkin
"""

from fastapi import APIRouter, Depends, Header, Query

from app.core.dependencies import DBDep
from app.db.repositories.guest_repository import (
    GuestCheckinRepository,
    GuestRepository,
    RoomRepository,
)
from app.schemas.guest.checkin import (
    GuestCheckinPrefillResponse,
    GuestCheckinSubmitRequest,
    GuestCheckinSubmitResponse,
)
from app.services.guest_checkin_service import GuestCheckinService

router = APIRouter(prefix="/guest/checkin", tags=["Guest — Check-In"])


def _get_service(db: DBDep) -> GuestCheckinService:
    return GuestCheckinService(
        guest_repo=GuestRepository(db),
        room_repo=RoomRepository(db),
        checkin_repo=GuestCheckinRepository(db),
    )


@router.get(
    "/prefill",
    response_model=GuestCheckinPrefillResponse,
    summary="Guest Check-In Prefill",
    description="Returns room context and current emergency profile for guest onboarding.",
)
async def get_prefill(
    service: GuestCheckinService = Depends(_get_service),
    guest_id: str | None = Query(default=None),
    x_guest_id: str | None = Header(default=None),
) -> GuestCheckinPrefillResponse:
    return await service.get_prefill(guest_id or x_guest_id)


@router.post(
    "",
    response_model=GuestCheckinSubmitResponse,
    summary="Submit Guest Check-In",
    description="Stores emergency profile details used during crisis response.",
)
async def submit_checkin(
    payload: GuestCheckinSubmitRequest,
    service: GuestCheckinService = Depends(_get_service),
) -> GuestCheckinSubmitResponse:
    return await service.submit_checkin(payload)
