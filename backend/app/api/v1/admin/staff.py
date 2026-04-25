"""
app/api/v1/admin/staff.py
"""

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.core.dependencies import AdminOnly, DBDep
from app.core.exceptions import NotFoundException
from app.db.repositories.admin_repository import PropertyRepository, StaffDirectoryRepository
from app.schemas.admin.staff_directory import (
    StaffDirectoryListResponse,
    StaffDirectoryMember,
    StaffExportResponse,
    StaffImportResponse,
)
from app.services.admin_staff_service import AdminStaffService

router = APIRouter(prefix="/admin/staff", tags=["Admin — Staff Directory"])


def _get_service(db: DBDep) -> AdminStaffService:
    return AdminStaffService(
        property_repo=PropertyRepository(db),
        staff_repo=StaffDirectoryRepository(db),
    )


@router.get(
    "",
    response_model=StaffDirectoryListResponse,
    summary="List Staff Directory",
)
async def list_staff(
    current_staff: dict = AdminOnly,
    service: AdminStaffService = Depends(_get_service),
    role: str | None = Query(default=None),
    status: str | None = Query(default=None),
    floor: int | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=200),
    property_id: str | None = Query(default=None),
) -> StaffDirectoryListResponse:
    return await service.list_staff(
        role=role,
        status=status,
        floor=floor,
        search=search,
        page=page,
        limit=limit,
        property_id=property_id,
    )


@router.post(
    "/import",
    response_model=StaffImportResponse,
    summary="Import Staff CSV",
)
async def import_staff(
    current_staff: dict = AdminOnly,
    service: AdminStaffService = Depends(_get_service),
    file: UploadFile = File(...),
    property_id: str = Form(...),
) -> StaffImportResponse:
    content = await file.read()
    return await service.import_staff(content, property_id)


@router.get(
    "/export",
    response_model=StaffExportResponse,
    summary="Export Staff CSV",
)
async def export_staff(
    current_staff: dict = AdminOnly,
    service: AdminStaffService = Depends(_get_service),
    property_id: str | None = Query(default=None),
) -> StaffExportResponse:
    return await service.export_staff(property_id)


@router.get(
    "/{employee_id}",
    response_model=StaffDirectoryMember,
    summary="Get Staff Member",
)
async def get_member(
    employee_id: str,
    current_staff: dict = AdminOnly,
    service: AdminStaffService = Depends(_get_service),
) -> StaffDirectoryMember:
    member = await service.get_member(employee_id)
    if not member:
        raise NotFoundException(message=f"Staff member '{employee_id}' not found.")
    return member
