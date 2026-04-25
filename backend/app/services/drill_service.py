"""
app/services/drill_service.py
Business logic for micro-training drills.
"""

from datetime import UTC, datetime

from app.core.constants import DRILL_PASSING_PERCENT
from app.core.exceptions import NotFoundException
from app.db.repositories.drill_repository import (
    DrillQuestionRepository,
    DrillRepository,
    DrillSessionRepository,
)
from app.schemas.staff.drill import (
    DrillAnswerRequest,
    DrillAnswerResponse,
    DrillCompleteResponse,
    DrillFeedback,
    DrillOption,
    DrillQuestion,
    DrillStartRequest,
    DrillStartResponse,
)


class DrillService:
    def __init__(
        self,
        drill_repo: DrillRepository,
        question_repo: DrillQuestionRepository,
        session_repo: DrillSessionRepository,
    ) -> None:
        self._drill_repo = drill_repo
        self._question_repo = question_repo
        self._session_repo = session_repo

    async def start_drill(self, request: DrillStartRequest) -> DrillStartResponse:
        drill = await self._drill_repo.get_by_drill_id(request.drill_id)
        if not drill:
            raise NotFoundException(message=f"Drill '{request.drill_id}' not found.")

        questions = await self._question_repo.list_for_drill(request.drill_id)
        if not questions:
            raise NotFoundException(message="This drill has no questions configured.")

        session_id = await self._session_repo.insert_one(
            {
                "drill_id": request.drill_id,
                "employee_id": request.employee_id,
                "started_at": datetime.now(UTC),
                "answers": [],
                "completed_at": None,
            }
        )

        first_q = self._to_question_schema(questions[0])

        return DrillStartResponse(
            session_id=session_id,
            drill_id=request.drill_id,
            title=drill["title"],
            total_questions=len(questions),
            first_question=first_q,
        )

    async def submit_answer(
        self, session_id: str, request: DrillAnswerRequest
    ) -> DrillAnswerResponse:
        session = await self._session_repo.get_by_session_id(session_id)
        if not session:
            raise NotFoundException(message="Drill session not found.")

        question = await self._question_repo.get_by_question_id(request.question_id)
        if not question:
            raise NotFoundException(message="Question not found.")

        correct_option_id: str = question["correct_option_id"]
        is_correct = request.selected_option_id == correct_option_id

        answer_record = {
            "question_id": request.question_id,
            "selected_option_id": request.selected_option_id,
            "correct": is_correct,
            "time_taken_seconds": request.time_taken_seconds,
            "answered_at": datetime.now(UTC),
        }
        await self._session_repo.append_answer(session_id, answer_record)

        # Find the next question
        all_questions = await self._question_repo.list_for_drill(session["drill_id"])
        answered_ids = {a["question_id"] for a in session.get("answers", [])}
        answered_ids.add(request.question_id)  # include the one just answered

        next_q_doc = next(
            (q for q in all_questions if q["question_id"] not in answered_ids), None
        )
        drill_complete = next_q_doc is None

        return DrillAnswerResponse(
            correct=is_correct,
            selected_option_id=request.selected_option_id,
            correct_option_id=correct_option_id,
            feedback=DrillFeedback(
                incorrect_text=question.get("feedback_incorrect") if not is_correct else None,
                correct_text=question.get("feedback_correct") if is_correct else None,
            ),
            next_question=self._to_question_schema(next_q_doc) if next_q_doc else None,
            drill_complete=drill_complete,
        )

    async def complete_drill(self, session_id: str) -> DrillCompleteResponse:
        session = await self._session_repo.get_by_session_id(session_id)
        if not session:
            raise NotFoundException(message="Drill session not found.")

        completed_at = datetime.now(UTC)
        await self._session_repo.update_one(
            {"_id": session_id},  # already converted by repo
            {"$set": {"completed_at": completed_at}},
        )

        answers = session.get("answers", [])
        total = len(answers)
        score = sum(1 for a in answers if a.get("correct"))
        percent = round((score / total * 100) if total > 0 else 0.0, 1)

        return DrillCompleteResponse(
            session_id=session_id,
            score=score,
            total=total,
            percent=percent,
            passed=percent >= DRILL_PASSING_PERCENT,
            completed_at=completed_at.isoformat(),
        )

    # ─── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _to_question_schema(doc: dict) -> DrillQuestion:
        return DrillQuestion(
            question_id=doc["question_id"],
            index=doc["index"],
            category=doc["category"],
            scenario_text=doc["scenario_text"],
            prompt=doc["prompt"],
            image_url=doc.get("image_url"),
            options=[
                DrillOption(option_id=o["option_id"], text=o["text"])
                for o in doc.get("options", [])
            ],
        )
