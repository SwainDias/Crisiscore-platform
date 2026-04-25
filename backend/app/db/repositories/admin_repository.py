"""
app/db/repositories/admin_repository.py
"""

import re
from datetime import datetime

from pymongo import ASCENDING, DESCENDING

from app.core.constants import Collection, StaffDirectoryStatus
from app.db.repositories.base_repository import BaseRepository


class PropertyRepository(BaseRepository):
    collection_name = Collection.PROPERTIES

    async def get_by_property_id(self, property_id: str) -> dict | None:
        return await self.find_one({"property_id": property_id})

    async def get_default(self) -> dict | None:
        docs = await self.find_many({}, limit=1)
        return docs[0] if docs else None


class StaffDirectoryRepository(BaseRepository):
    collection_name = Collection.STAFF

    async def count_on_shift(self, property_id: str) -> int:
        return await self.count({"property_id": property_id, "duty_status": {"$ne": "off_duty"}})

    async def list_staff(
        self,
        property_id: str,
        role: str | None,
        status: str | None,
        floor: int | None,
        search: str | None,
        page: int,
        limit: int,
    ) -> tuple[list[dict], int]:
        query: dict = {"property_id": property_id}
        if role:
            query["role"] = role
        if status:
            query["status"] = status
        if floor is not None:
            query["assignment.floor"] = floor
        if search:
            safe_search = re.escape(search)
            query["$or"] = [
                {"name": {"$regex": safe_search, "$options": "i"}},
                {"employee_id": {"$regex": safe_search, "$options": "i"}},
            ]

        skip = max(page - 1, 0) * limit
        total = await self.count(query)
        rows = await self.find_many(
            query,
            sort=[("last_seen_at", DESCENDING), ("updated_at", DESCENDING)],
            limit=limit,
            skip=skip,
        )
        return rows, total

    async def list_active_responders(self, property_id: str, limit: int = 20) -> list[dict]:
        return await self.find_many(
            {
                "property_id": property_id,
                "status": {"$in": [StaffDirectoryStatus.RESPONDING, StaffDirectoryStatus.AVAILABLE]},
                "duty_status": {"$ne": "off_duty"},
            },
            sort=[("updated_at", DESCENDING)],
            limit=limit,
        )

    async def get_by_employee_id(self, employee_id: str) -> dict | None:
        return await self.find_one({"employee_id": employee_id})


class BroadcastRepository(BaseRepository):
    collection_name = Collection.BROADCASTS

    async def count_recipients_for_audience(
        self,
        property_id: str,
        audience: str,
        room_id: str | None,
        floor: int | None,
        guest_repo: BaseRepository,
    ) -> int:
        guest_query: dict = {"property_id": property_id}
        if audience == "specific_room" and room_id:
            guest_query["room_id"] = room_id
        if audience == "affected_floor" and floor is not None:
            guest_query["floor"] = floor
        return await guest_repo.count(guest_query)


class IntegrationRepository(BaseRepository):
    collection_name = Collection.INTEGRATIONS

    async def get_by_integration_id(self, integration_id: str) -> dict | None:
        return await self.find_one({"integration_id": integration_id})

    async def list_all(self) -> list[dict]:
        return await self.find_many({}, sort=[("name", ASCENDING)], limit=500)


class SettingsRepository(BaseRepository):
    collection_name = Collection.SETTINGS

    async def get_by_key(self, key: str) -> dict | None:
        return await self.find_one({"key": key})


class UserRoleRepository(BaseRepository):
    collection_name = Collection.USER_ROLES

    async def list_users(self) -> list[dict]:
        return await self.find_many({}, sort=[("name", ASCENDING)], limit=500)


class ProtocolRepository(BaseRepository):
    collection_name = Collection.PROTOCOLS

    async def list_protocols(self) -> list[dict]:
        return await self.find_many({}, sort=[("name", ASCENDING)], limit=500)


class CCTVCameraRepository(BaseRepository):
    collection_name = Collection.CCTV_CAMERAS

    async def list_for_floor(self, property_id: str, floor: int) -> list[dict]:
        return await self.find_many(
            {"property_id": property_id, "floor": floor},
            sort=[("camera_id", ASCENDING)],
            limit=300,
        )


class ResponderAssignmentRepository(BaseRepository):
    collection_name = Collection.RESPONDER_ASSIGNMENTS

    async def list_for_incident(self, incident_id: str) -> list[dict]:
        return await self.find_many(
            {"incident_id": incident_id},
            sort=[("created_at", ASCENDING)],
            limit=500,
        )


class IncidentLogRepository(BaseRepository):
    collection_name = Collection.INCIDENT_LOGS

    async def list_for_incident(self, incident_id: str, limit: int = 200) -> list[dict]:
        return await self.find_many(
            {"incident_id": incident_id},
            sort=[("timestamp", DESCENDING)],
            limit=limit,
        )

    async def create_log(self, incident_id: str, payload: dict) -> str:
        entry = {
            "incident_id": incident_id,
            "timestamp": payload.get("timestamp", datetime.utcnow().isoformat()),
            **payload,
        }
        return await self.insert_one(entry)
