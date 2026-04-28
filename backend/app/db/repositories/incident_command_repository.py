"""
app/db/repositories/incident_command_repository.py
"""

from datetime import datetime

from bson import ObjectId
from pymongo import DESCENDING

from app.core.constants import Collection, IncidentStatus
from app.db.repositories.base_repository import BaseRepository


class IncidentCommandRepository(BaseRepository):
    collection_name = Collection.INCIDENTS

    async def get_by_incident_id(self, incident_id: str) -> dict | None:
        doc = await self.find_one({"incident_id": incident_id})
        if doc:
            return doc

        try:
            oid = ObjectId(incident_id)
        except Exception:
            return None
        return await self.find_one({"_id": oid})

    async def list_for_property(
        self,
        property_id: str,
        limit: int = 50,
        include_resolved: bool = True,
    ) -> list[dict]:
        query: dict = {"property_id": property_id}
        if not include_resolved:
            query["status"] = {"$ne": IncidentStatus.RESOLVED}
        return await self.find_many(
            query,
            sort=[("created_at", DESCENDING)],
            limit=limit,
        )

    async def count_active(self, property_id: str) -> int:
        return await self.count(
            {
                "property_id": property_id,
                "status": {"$in": [IncidentStatus.ACTIVE, IncidentStatus.CONTAINED, IncidentStatus.INVESTIGATING]},
            }
        )

    async def set_status(
        self,
        incident_id: str,
        status: str,
        timestamp: datetime,
        resolved_by: str | None = None,
        resolution_note: str | None = None,
    ) -> bool:
        update_fields: dict = {
            "status": status,
            "updated_at": timestamp,
        }
        if status == IncidentStatus.RESOLVED:
            update_fields["resolved_at"] = timestamp
            update_fields["concluded_at"] = timestamp
            update_fields["resolved_by"] = resolved_by
            update_fields["resolution_note"] = resolution_note

        return await self.update_one(
            {"incident_id": incident_id},
            {"$set": update_fields},
        )

    async def resolve_all_active(self) -> int:
        return await self.update_many(
            {"status": {"$ne": IncidentStatus.RESOLVED}},
            {"$set": {"status": IncidentStatus.RESOLVED, "resolved_at": self._now()}},
        )

    async def set_severity(
        self,
        incident_id: str,
        severity: str,
        escalated_by: str,
        reason: str,
        timestamp: datetime,
    ) -> bool:
        timeline_entry = {
            "event_id": f"evt-{timestamp.timestamp()}",
            "timestamp": timestamp,
            "title": "Incident escalated",
            "description": f"Escalated to {severity} by {escalated_by}: {reason}",
            "icon_type": "alert",
        }
        result = await self._col.update_one(
            {"incident_id": incident_id},
            {
                "$set": {"severity": severity, "updated_at": timestamp},
                "$push": {"timeline": timeline_entry},
            },
        )
        return result.modified_count > 0

    async def append_log(self, incident_id: str, log_entry: dict) -> bool:
        result = await self._col.update_one(
            {"incident_id": incident_id},
            {
                "$push": {"timeline": log_entry},
                "$set": {"updated_at": self._now()},
            },
        )
        return result.modified_count > 0

    async def upsert_guest_status(
        self,
        incident_id: str,
        guest_id: str,
        guest_status: dict,
    ) -> bool:
        incident = await self.get_by_incident_id(incident_id)
        if not incident:
            return False

        accountability = incident.get("guest_accountability", [])
        updated = False
        for idx, item in enumerate(accountability):
            if item.get("guest_id") == guest_id:
                accountability[idx] = {**item, **guest_status}
                updated = True
                break

        if not updated:
            accountability.append({"guest_id": guest_id, **guest_status})

        return await self.update_one(
            {"incident_id": incident_id},
            {"$set": {"guest_accountability": accountability}},
        )

    async def upsert_responder_assignment(
        self,
        incident_id: str,
        employee_id: str,
        assignment: dict,
    ) -> bool:
        incident = await self.get_by_incident_id(incident_id)
        if not incident:
            return False

        assignments = incident.get("responder_assignments", [])
        updated = False
        for idx, item in enumerate(assignments):
            if item.get("employee_id") == employee_id:
                assignments[idx] = {**item, **assignment}
                updated = True
                break

        if not updated:
            assignments.append({"employee_id": employee_id, **assignment})

        return await self.update_one(
            {"incident_id": incident_id},
            {"$set": {"responder_assignments": assignments}},
        )
