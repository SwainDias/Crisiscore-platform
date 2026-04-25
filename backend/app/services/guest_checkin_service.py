"""
app/services/guest_checkin_service.py
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import GuestErrorCode
from app.core.exceptions import NotFoundException
from app.db.repositories.guest_repository import GuestCheckinRepository, GuestRepository, RoomRepository
from app.schemas.guest.checkin import (
    ExistingEmergencyProfile,
    GuestCheckinPrefillResponse,
    GuestCheckinSubmitRequest,
    GuestCheckinSubmitResponse,
    PrefillRoom,
)


class GuestCheckinService:
    def __init__(
        self,
        guest_repo: GuestRepository,
        room_repo: RoomRepository,
        checkin_repo: GuestCheckinRepository,
    ) -> None:
        self._guest_repo = guest_repo
        self._room_repo = room_repo
        self._checkin_repo = checkin_repo

    async def get_prefill(self, guest_id: str | None = None) -> GuestCheckinPrefillResponse:
        guest = await self._resolve_guest(guest_id)

        room = await self._room_repo.get_by_room_id(guest.get("room_id", ""))
        if not room:
            room = {
                "room_id": guest.get("room_id", "ROOM-UNKNOWN"),
                "room_number": guest.get("room_number", "Unknown"),
                "wing": guest.get("wing", "A"),
                "floor": int(guest.get("floor", 0)),
            }

        profile = guest.get("emergency_profile", {})
        return GuestCheckinPrefillResponse(
            guest_id=guest["guest_id"],
            room=PrefillRoom(
                room_id=room.get("room_id", guest.get("room_id", "ROOM-UNKNOWN")),
                room_number=room.get("room_number", "Unknown"),
                wing=room.get("wing", "A"),
                floor=int(room.get("floor", 0)),
            ),
            existing_profile=ExistingEmergencyProfile(
                blood_type=profile.get("blood_type"),
                mobility_needs=profile.get("mobility_needs", []),
                medical_notes=profile.get("medical_notes"),
            ),
        )

    async def submit_checkin(
        self,
        request: GuestCheckinSubmitRequest,
    ) -> GuestCheckinSubmitResponse:
        guest = await self._guest_repo.get_by_guest_id(request.guest_id)
        if not guest:
            raise NotFoundException(
                code=GuestErrorCode.GUEST_NOT_FOUND,
                message=f"Guest '{request.guest_id}' not found.",
            )

        room = await self._room_repo.get_by_room_id(request.room_id)
        if not room:
            raise NotFoundException(
                code=GuestErrorCode.CHECKIN_NOT_FOUND,
                message=f"Room '{request.room_id}' not found.",
            )

        emergency_profile = request.emergency_profile.model_dump()

        await self._guest_repo.update_one(
            {"guest_id": request.guest_id},
            {
                "$set": {
                    "room_id": request.room_id,
                    "room_number": room.get("room_number"),
                    "floor": room.get("floor"),
                    "wing": room.get("wing"),
                    "emergency_profile": emergency_profile,
                }
            },
            upsert=True,
        )

        checkin_id = str(uuid.uuid4())
        await self._checkin_repo.insert_one(
            {
                "checkin_id": checkin_id,
                "guest_id": request.guest_id,
                "room_id": request.room_id,
                "property_id": guest.get("property_id"),
                "emergency_profile": emergency_profile,
                "created_at": datetime.now(UTC),
            }
        )

        return GuestCheckinSubmitResponse(
            success=True,
            checkin_id=checkin_id,
            next_route="/guest/home",
        )

    async def _resolve_guest(self, guest_id: str | None) -> dict:
        guest = None
        if guest_id:
            guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            guest = await self._guest_repo.get_default()
        if not guest:
            raise NotFoundException(
                code=GuestErrorCode.GUEST_NOT_FOUND,
                message="Guest profile not found.",
            )
        return guest
