"""
app/services/alert_service.py
Business logic for raising and managing alerts.
Shared by both staff and guest API routes.
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import AlertErrorCode, IncidentStatus
from app.core.exceptions import (
    DuplicateAlertException,
    NotFoundException,
    ServiceUnavailableException,
)
from app.db.repositories.alert_repository import AlertRepository, AlertTypeRepository
from app.db.repositories.incident_repository import IncidentRepository
from app.schemas.shared.alert import (
    AlertTypeItem,
    AlertTypesResponse,
    RaiseAlertRequest,
    RaiseAlertResponse,
)


class AlertService:
    def __init__(
        self,
        alert_repo: AlertRepository,
        alert_type_repo: AlertTypeRepository,
        incident_repo: IncidentRepository,
    ) -> None:
        self._alert_repo = alert_repo
        self._alert_type_repo = alert_type_repo
        self._incident_repo = incident_repo

    async def get_alert_types(self) -> AlertTypesResponse:
        docs = await self._alert_type_repo.get_all_active()
        types = [
            AlertTypeItem(
                type_id=d["type_id"],
                label=d["label"],
                description=d["description"],
                icon=d.get("icon", "alert-circle"),
                color_hex=d.get("color_hex", "#FF0000"),
                severity_default=d["severity_default"],
            )
            for d in docs
        ]
        return AlertTypesResponse(types=types)

    async def raise_alert(self, request: RaiseAlertRequest) -> RaiseAlertResponse:
        # ── Validate alert type ───────────────────────────────────────────────
        alert_type = await self._alert_type_repo.get_by_type_id(request.type_id)
        if not alert_type:
            raise NotFoundException(
                code=AlertErrorCode.ALERT_TYPE_NOT_FOUND,
                message=f"Alert type '{request.type_id}' not found.",
            )

        # ── Duplicate guard ───────────────────────────────────────────────────
        duplicate = await self._alert_repo.get_recent_duplicate(
            user_id=request.raised_by.user_id,
            type_id=request.type_id,
        )
        if duplicate:
            raise DuplicateAlertException()

        # ── Persist alert ─────────────────────────────────────────────────────
        alert_id = str(uuid.uuid4())
        alert_data = {
            "alert_id": alert_id,
            "type_id": request.type_id,
            "additional_details": request.additional_details,
            "location": request.location.model_dump(),
            "raised_by": request.raised_by.model_dump(),
            "device_id": request.device_id,
            "raised_at": datetime.fromisoformat(request.timestamp),
            "severity": alert_type["severity_default"],
            "status": "active",
        }

        # ── Attach to or create an incident ───────────────────────────────────
        incident_id = await self._attach_to_incident(alert_data, alert_type)
        alert_data["incident_id"] = incident_id

        await self._alert_repo.insert_one(alert_data)

        # ── Notify responders ─────────────────────────────────────────────────
        responders_notified = await self._dispatch_notifications(alert_data, alert_type)

        return RaiseAlertResponse(
            success=True,
            alert_id=alert_id,
            incident_id=incident_id,
            message="Alert raised successfully. Help is on the way.",
            responders_notified=responders_notified,
            next_route=f"/incidents/{incident_id}" if incident_id else "/home",
        )

    # ─── Private helpers ──────────────────────────────────────────────────────

    async def _attach_to_incident(
        self, alert_data: dict, alert_type: dict
    ) -> str | None:
        """
        If a critical alert type is raised, ensure an active incident exists.
        Returns the incident_id (new or existing).
        """
        severity = alert_type.get("severity_default", "info")
        if severity not in ("warning", "critical"):
            return None

        # Try to find an existing active incident for the property
        # In a real system we'd derive property_id from the auth token / location
        property_id = alert_data.get("raised_by", {}).get("property_id", "DEFAULT")

        existing = await self._incident_repo.get_active_for_property(property_id)
        if existing:
            return existing.get("id")

        # Create a new incident
        incident_id = str(uuid.uuid4())
        await self._incident_repo.insert_one(
            {
                "incident_id": incident_id,
                "property_id": property_id,
                "title": f"{alert_type['label']} Alert",
                "description": alert_data.get("additional_details", ""),
                "severity": severity,
                "status": IncidentStatus.ACTIVE,
                "event_code": f"EVT-{alert_type['type_id'].upper()}",
                "alert_ids": [alert_data["alert_id"]],
                "zones_affected": 0,
                "units_deployed": 0,
                "timeline": [],
                "improvement_opportunities": [],
                "kpis": {},
            }
        )
        return incident_id

    async def _dispatch_notifications(self, alert_data: dict, alert_type: dict) -> int:
        """
        Stub — in production this would fan out to:
        - Role-based push notifications (FCM / APNs)
        - WhatsApp Business API for residents
        - IoT actuator triggers (smart locks, gas valves)
        Returns the number of responders notified.
        """
        return 3
