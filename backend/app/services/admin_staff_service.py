"""
app/services/admin_staff_service.py
"""

import csv
import io
from datetime import UTC, datetime, timedelta

from app.core.security import hash_password
from app.db.repositories.admin_repository import PropertyRepository, StaffDirectoryRepository
from app.schemas.admin.staff_directory import (
    FilterRoleOption,
    StaffAssignment,
    StaffDirectoryListResponse,
    StaffDirectoryMember,
    StaffDirectorySummary,
    StaffExportResponse,
    StaffFilterOptions,
    StaffImportResponse,
    StaffPagination,
    UnresponsiveAlert,
)


class AdminStaffService:
    def __init__(
        self,
        property_repo: PropertyRepository,
        staff_repo: StaffDirectoryRepository,
    ) -> None:
        self._property_repo = property_repo
        self._staff_repo = staff_repo

    async def list_staff(
        self,
        role: str | None,
        status: str | None,
        floor: int | None,
        search: str | None,
        page: int,
        limit: int,
        property_id: str | None = None,
    ) -> StaffDirectoryListResponse:
        property_doc = await self._resolve_property(property_id)
        pid = property_doc["property_id"]

        rows, total = await self._staff_repo.list_staff(
            property_id=pid,
            role=role,
            status=status,
            floor=floor,
            search=search,
            page=page,
            limit=limit,
        )

        all_rows, _ = await self._staff_repo.list_staff(
            property_id=pid,
            role=None,
            status=None,
            floor=None,
            search=None,
            page=1,
            limit=1000,
        )

        unresponsive_count = len([r for r in all_rows if r.get("status") == "unresponsive"])
        on_shift_count = len([r for r in all_rows if r.get("duty_status") != "off_duty"])

        total_pages = (total + limit - 1) // limit if total > 0 else 1

        return StaffDirectoryListResponse(
            summary=StaffDirectorySummary(
                total=total,
                on_shift=on_shift_count,
                unresponsive=unresponsive_count,
            ),
            unresponsive_alert=UnresponsiveAlert(
                present=unresponsive_count > 0,
                count=unresponsive_count if unresponsive_count > 0 else None,
                message=(
                    f"{unresponsive_count} staff members are currently unresponsive."
                    if unresponsive_count > 0
                    else None
                ),
            ),
            staff=[self._to_member(row) for row in rows],
            pagination=StaffPagination(page=page, limit=limit, total_pages=total_pages),
            filter_options=self._filter_options(all_rows),
        )

    async def import_staff(
        self,
        file_content: bytes,
        property_id: str,
    ) -> StaffImportResponse:
        text = file_content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))

        imported = 0
        errors: list[str] = []

        for index, row in enumerate(reader, start=2):
            employee_id = (row.get("employee_id") or "").strip()
            name = (row.get("name") or "").strip()
            role = (row.get("role") or "responder").strip()

            if not employee_id or not name:
                errors.append(f"Line {index}: employee_id and name are required")
                continue

            payload = {
                "employee_id": employee_id,
                "name": name,
                "phone": (row.get("phone") or "").strip(),
                "role": role,
                "role_id": (row.get("role_id") or role.upper()).strip(),
                "property_id": property_id,
                "duty_status": (row.get("duty_status") or "on_duty").strip(),
                "status": (row.get("status") or "available").strip(),
                "assignment": {
                    "label": (row.get("assignment_label") or "Unassigned").strip(),
                    "floor": int(row.get("floor") or 0) if (row.get("floor") or "").strip() else None,
                    "zone": (row.get("zone") or "").strip() or None,
                },
                "pin_hash": hash_password((row.get("pin") or "1234").strip()),
                "last_seen_at": datetime.now(UTC).isoformat(),
            }

            await self._staff_repo.update_one(
                {"employee_id": employee_id},
                {"$set": payload},
                upsert=True,
            )
            imported += 1

        return StaffImportResponse(success=len(errors) == 0, imported=imported, errors=errors)

    async def export_staff(self, property_id: str | None = None) -> StaffExportResponse:
        property_doc = await self._resolve_property(property_id)
        pid = property_doc["property_id"]

        expires_at = (datetime.now(UTC) + timedelta(hours=2)).isoformat()
        return StaffExportResponse(
            file_url=f"https://cdn.example.com/exports/{pid}/staff.csv",
            expires_at=expires_at,
        )

    async def get_member(self, employee_id: str) -> StaffDirectoryMember | None:
        row = await self._staff_repo.get_by_employee_id(employee_id)
        if not row:
            return None
        return self._to_member(row)

    async def _resolve_property(self, property_id: str | None) -> dict:
        property_doc = None
        if property_id:
            property_doc = await self._property_repo.get_by_property_id(property_id)
        if not property_doc:
            property_doc = await self._property_repo.get_default()
        if not property_doc:
            property_doc = {"property_id": "PROP-DEFAULT", "name": "Rapid Response Property"}
        return property_doc

    @staticmethod
    def _to_member(row: dict) -> StaffDirectoryMember:
        assignment = row.get("assignment", {})
        fallback_assignment = {
            "label": row.get("assignment_label", "Unassigned"),
            "floor": row.get("floor"),
            "zone": row.get("zone"),
        }
        assignment_data = assignment if assignment else fallback_assignment

        return StaffDirectoryMember(
            employee_id=row.get("employee_id", ""),
            name=row.get("name", "Staff"),
            phone=row.get("phone", ""),
            avatar_url=row.get("avatar_url"),
            role=row.get("role", "responder"),
            role_id=row.get("role_id", row.get("role", "RESPONDER").upper()),
            assignment=StaffAssignment(
                label=assignment_data.get("label", "Unassigned"),
                floor=assignment_data.get("floor"),
                zone=assignment_data.get("zone"),
            ),
            last_seen_at=str(row.get("last_seen_at", datetime.now(UTC).isoformat())),
            status=row.get("status", "available"),
            response_time_seconds=row.get("response_time_seconds"),
        )

    @staticmethod
    def _filter_options(rows: list[dict]) -> StaffFilterOptions:
        role_counts: dict[str, int] = {}
        floors: set[int] = set()
        for row in rows:
            role = row.get("role", "responder")
            role_counts[role] = role_counts.get(role, 0) + 1

            assignment = row.get("assignment", {})
            floor = assignment.get("floor")
            if floor is None:
                floor = row.get("floor")
            if isinstance(floor, int):
                floors.add(floor)

        role_options = [
            FilterRoleOption(label=role.replace("_", " ").title(), value=role, count=count)
            for role, count in sorted(role_counts.items())
        ]

        return StaffFilterOptions(
            roles=role_options,
            statuses=["available", "responding", "unresponsive"],
            floors=sorted(list(floors)),
        )
