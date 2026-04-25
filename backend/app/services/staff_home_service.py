"""
app/services/staff_home_service.py
Business logic for the Staff Home / Status Dashboard page.
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import (
    DutyStatus,
    IncidentSeverity,
    IncidentStatus,
    SOS_BROADCAST_CHANNEL,
)
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.staff_repository import StaffRepository
from app.db.repositories.task_repository import TaskRepository
from app.schemas.staff.home import (
    ActiveIncident,
    Assignment,
    HistoryLog,
    LiveMap,
    MyStatus,
    SOSTriggerRequest,
    SOSTriggerResponse,
    StaffHomeResponse,
    StaffSummary,
    TaskItem,
)


class StaffHomeService:
    def __init__(
        self,
        staff_repo: StaffRepository,
        incident_repo: IncidentRepository,
        task_repo: TaskRepository,
    ) -> None:
        self._staff_repo = staff_repo
        self._incident_repo = incident_repo
        self._task_repo = task_repo

    async def get_home(self, employee_id: str) -> StaffHomeResponse:
        staff = await self._staff_repo.get_by_employee_id(employee_id)
        if not staff:
            from app.core.exceptions import NotFoundException
            raise NotFoundException(message="Staff member not found.")

        # ── Active incident ───────────────────────────────────────────────────
        active_incident_doc = await self._incident_repo.get_active_for_property(
            staff["property_id"]
        )
        active_incident = self._build_active_incident(active_incident_doc)

        # ── Tasks ─────────────────────────────────────────────────────────────
        task_docs = await self._task_repo.list_for_staff(employee_id)
        tasks_total = await self._task_repo.count_for_staff(employee_id)
        tasks = [
            TaskItem(
                task_id=t.get("task_id", str(t.get("id", ""))),
                title=t["title"],
                priority=t["priority"],
                status=t["status"],
                due_at=t.get("due_at"),
            )
            for t in task_docs
        ]

        # ── Shift / duty status ───────────────────────────────────────────────
        my_status = MyStatus(
            duty_status=staff.get("duty_status", DutyStatus.ON_DUTY),
            assignment=Assignment(
                assignment_id=staff.get("assignment_id", "ZONE-DEFAULT"),
                label=staff.get("assignment_label", "Main Gate"),
            ),
            checkin_time=staff.get("checkin_time", datetime.now(UTC).isoformat()),
            vehicle=staff.get("vehicle"),
        )

        return StaffHomeResponse(
            staff=StaffSummary(
                employee_id=staff["employee_id"],
                name=staff["name"],
                avatar_url=staff.get("avatar_url"),
            ),
            active_incident=active_incident,
            my_status=my_status,
            sos_enabled=True,
            live_map=LiveMap(
                active_zones=active_incident_doc["zones_affected"]
                if active_incident_doc
                else 0,
                units_deployed=active_incident_doc.get("units_deployed", 0)
                if active_incident_doc
                else 0,
                map_preview_url=None,
                route="/map/live",
            ),
            my_tasks=tasks,
            tasks_total=tasks_total,
            history=await self._build_recent_history(employee_id),
        )

    async def trigger_sos(self, request: SOSTriggerRequest) -> SOSTriggerResponse:
        """
        Publishes an SOS broadcast.  In production this would publish to a
        Redis pub/sub channel or a push notification service.
        """
        broadcast_id = str(uuid.uuid4())
        # TODO: publish to SOS_BROADCAST_CHANNEL via Redis
        return SOSTriggerResponse(broadcast_id=broadcast_id, acknowledged=True)

    # ─── Helpers ─────────────────────────────────────────────────────────────

    def _build_active_incident(self, doc: dict | None) -> ActiveIncident:
        if not doc:
            return ActiveIncident(present=False)
        return ActiveIncident(
            present=True,
            incident_id=doc.get("id"),
            title=doc.get("title"),
            body=doc.get("description"),
            severity=doc.get("severity", IncidentSeverity.WARNING),
            cta_route=f"/incidents/{doc.get('id')}",
        )

    async def _build_recent_history(self, employee_id: str) -> list[HistoryLog]:
        # Placeholder — in production query an activity_logs collection
        return []
