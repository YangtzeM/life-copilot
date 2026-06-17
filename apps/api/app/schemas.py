from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models import TaskPriority, TaskStatus


class TaskCaptureRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


class ParsedTask(BaseModel):
    title: str
    description: str
    priority: TaskPriority
    due_at: datetime | None = None
    reminder_at: datetime | None = None
    review_at: datetime | None = None
    smallest_next_action: str
    token_estimate: int
    provider_name: str


class TaskResponse(BaseModel):
    id: UUID
    raw_text: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    due_at: datetime | None
    reminder_at: datetime | None
    review_at: datetime | None


class PlanStep(BaseModel):
    order: int
    title: str
    description: str


class PlanResponse(BaseModel):
    id: UUID
    task_id: UUID
    summary: str
    steps: list[PlanStep]
    token_estimate: int
    provider_name: str


class CaptureTaskResponse(BaseModel):
    task: TaskResponse
    parsed: ParsedTask


class GeneratePlanRequest(BaseModel):
    task_id: UUID

