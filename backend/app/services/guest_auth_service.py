"""
app/services/guest_auth_service.py
Lightweight auth for resident/guest — no PIN, token issued based on
guest_id + property_network_id during check-in flow.
"""

from app.core.security import create_access_token, create_refresh_token
from app.core.exceptions import UnauthorizedException
from app.core.constants import AuthErrorCode
from app.db.repositories.guest_repository import GuestRepository


class GuestAuthService:
    def __init__(self, guest_repo: GuestRepository) -> None:
        self._guest_repo = guest_repo

    async def issue_token(self, guest_id: str, device_id: str) -> dict:
        guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            raise UnauthorizedException(
                code=AuthErrorCode.INVALID_CREDENTIALS,
                message="Guest not found. Please complete check-in first.",
            )

        access_token, expires_in = create_access_token(
            guest_id,
            extra={"user_type": "guest", "property_id": guest["property_id"]},
        )
        refresh_token = create_refresh_token(guest_id)

        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "guest": {
                "guest_id": guest_id,
                "name": guest.get("name", "Resident"),
                "room_id": guest.get("room_id"),
                "property_id": guest.get("property_id"),
            },
        }
