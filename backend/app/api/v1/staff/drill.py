"""
app/api/v1/staff/drill.py
POST /api/v1/staff/drill/start
POST /api/v1/staff/drill/{session_id}/answer
POST /api/v1/staff/drill/{session_id}/complete
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentStaff, DBDep
from app.db.repositories.drill_repository import (
    DrillQuestionRepository,
    DrillRepository,
    DrillSessionRepository,
)
from app.schemas.staff.drill import (
    DrillAnswerRequest,
    DrillAnswerResponse,
    DrillCompleteResponse,
    DrillStartRequest,
    DrillStartResponse,
)
from app.services.drill_service import DrillService

router = APIRouter(prefix="/staff/drill", tags=["Staff — Micro Drill"])


def _get_service(db: DBDep) -> DrillService:
    return DrillService(
        DrillRepository(db),
        DrillQuestionRepository(db),
        DrillSessionRepository(db),
    )


@router.post(
    "/start",
    response_model=DrillStartResponse,
    summary="Start Micro-Drill Session",
    description=(
        "Initialises a new drill session for the authenticated staff member and "
        "returns the first question."
    ),
)
async def start_drill(
    payload: DrillStartRequest,
    current_staff: CurrentStaff,
    service: DrillService = Depends(_get_service),
) -> DrillStartResponse:
    return await service.start_drill(payload)


@router.post(
    "/{session_id}/answer",
    response_model=DrillAnswerResponse,
    summary="Submit Drill Answer",
    description=(
        "Submits the staff member's answer to the current question. Returns "
        "correctness feedback and the next question (or signals drill completion)."
    ),
)
async def submit_answer(
    session_id: str,
    payload: DrillAnswerRequest,
    current_staff: CurrentStaff,
    service: DrillService = Depends(_get_service),
) -> DrillAnswerResponse:
    return await service.submit_answer(session_id, payload)


@router.post(
    "/{session_id}/complete",
    response_model=DrillCompleteResponse,
    summary="Complete Drill Session",
    description=(
        "Finalises the drill session, calculates the score, and marks the session "
        "as complete. Returns pass/fail result."
    ),
)
async def complete_drill(
    session_id: str,
    current_staff: CurrentStaff,
    service: DrillService = Depends(_get_service),
) -> DrillCompleteResponse:
    return await service.complete_drill(session_id)
