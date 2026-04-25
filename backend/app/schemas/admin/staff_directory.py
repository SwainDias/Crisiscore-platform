"""
app/schemas/admin/staff_directory.py
"""

from pydantic import BaseModel

from app.core.constants import StaffOperationalStatus


class StaffAssignment(BaseModel):
    label: str
    floor: int | None = None
    zone: str | None = None


class StaffDirectoryEntry(BaseModel):
    employee_id: str
    name: str
    phone: str
    avatar_url: str | None = None
    role: str
    role_id: str
    assignment: StaffAssignment
    last_seen_at: str
    status: StaffOperationalStatus
    response_time_seconds: int | None = None


class DirectorySummary(BaseModel):
    total: int
    on_shift: int
    unresponsive: int


class UnresponsiveAlert(BaseModel):
    present: bool
    count: int | None = None
    message: str | None = None


class Pagination(BaseModel):
    page: int
    limit: int
    total_pages: int


class RoleFilterOption(BaseModel):
    label: str
    value: str
    count: int


class FilterOptions(BaseModel):
    roles: list[RoleFilterOption]
    statuses: list[str]
    floors: list[int]


class StaffDirectoryResponse(BaseModel):
    summary: DirectorySummary
    unresponsive_alert: UnresponsiveAlert
    staff: list[StaffDirectoryEntry]
    pagination: Pagination
    filter_options: FilterOptions


class StaffImportResponse(BaseModel):
    success: bool
    imported: int
    errors: list[str]


class StaffExportResponse(BaseModel):
    file_url: str
    expires_at: str
