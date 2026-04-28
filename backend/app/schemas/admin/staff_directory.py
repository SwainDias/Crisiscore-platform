"""
app/schemas/admin/staff_directory.py
"""

from pydantic import BaseModel

from app.core.constants import StaffDirectoryStatus


class StaffDirectorySummary(BaseModel):
    total: int
    on_shift: int
    unresponsive: int


class UnresponsiveAlert(BaseModel):
    present: bool
    count: int | None = None
    message: str | None = None


class StaffAssignment(BaseModel):
    label: str
    floor: int | None = None
    zone: str | None = None


class StaffDirectoryMember(BaseModel):
    employee_id: str
    name: str
    phone: str
    avatar_url: str | None = None
    role: str
    role_id: str
    assignment: StaffAssignment
    last_seen_at: str
    status: StaffDirectoryStatus
    response_time_seconds: int | None = None


class StaffPagination(BaseModel):
    page: int
    limit: int
    total_pages: int


class FilterRoleOption(BaseModel):
    label: str
    value: str
    count: int


class StaffFilterOptions(BaseModel):
    roles: list[FilterRoleOption]
    statuses: list[str]
    floors: list[int]


class StaffDirectoryListResponse(BaseModel):
    summary: StaffDirectorySummary
    unresponsive_alert: UnresponsiveAlert
    staff: list[StaffDirectoryMember]
    pagination: StaffPagination
    filter_options: StaffFilterOptions


class StaffImportResponse(BaseModel):
    success: bool
    imported: int
    errors: list[str]


class StaffExportResponse(BaseModel):
    file_url: str
    expires_at: str
