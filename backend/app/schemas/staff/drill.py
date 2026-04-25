"""
app/schemas/staff/drill.py
"""

from pydantic import BaseModel


class DrillStartRequest(BaseModel):
    employee_id: str
    drill_id: str


class DrillOption(BaseModel):
    option_id: str
    text: str


class DrillQuestion(BaseModel):
    question_id: str
    index: int
    category: str
    scenario_text: str
    prompt: str
    image_url: str | None = None
    options: list[DrillOption]


class DrillStartResponse(BaseModel):
    session_id: str
    drill_id: str
    title: str
    total_questions: int
    first_question: DrillQuestion


class DrillAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    selected_option_id: str
    time_taken_seconds: int


class DrillFeedback(BaseModel):
    incorrect_text: str | None = None
    correct_text: str | None = None


class DrillAnswerResponse(BaseModel):
    correct: bool
    selected_option_id: str
    correct_option_id: str
    feedback: DrillFeedback
    next_question: DrillQuestion | None = None
    drill_complete: bool


class DrillCompleteResponse(BaseModel):
    session_id: str
    score: int
    total: int
    percent: float
    passed: bool
    completed_at: str
