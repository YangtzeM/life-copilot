from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from app.config import get_settings
from app.db import get_session, init_db
from app.model_provider import ModelProvider, get_model_provider
from app.models import Plan, Reminder, Task, TaskStatus
from app.schemas import (
    CaptureTaskResponse,
    GeneratePlanRequest,
    ParsedTask,
    PlanResponse,
    TaskCaptureRequest,
    TaskResponse,
)
from app.tasks import request_review, send_reminder


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


app = FastAPI(title="Life Copilot API", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tasks/capture", response_model=CaptureTaskResponse)
def capture_task(
    payload: TaskCaptureRequest,
    session: Session = Depends(get_session),
    provider: ModelProvider = Depends(get_model_provider),
) -> CaptureTaskResponse:
    parsed = provider.parse_task(payload.text)
    task = Task(
        raw_text=payload.text,
        title=parsed.title,
        description=parsed.description,
        priority=parsed.priority,
        due_at=parsed.due_at,
        reminder_at=parsed.reminder_at,
        review_at=parsed.review_at,
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    if task.reminder_at:
        reminder = Reminder(task_id=task.id, remind_at=task.reminder_at, message=f"Next action: {parsed.smallest_next_action}")
        session.add(reminder)
        session.commit()
        session.refresh(reminder)
        if get_settings().enqueue_tasks:
            send_reminder.apply_async(args=[str(reminder.id)], eta=task.reminder_at)

    if task.review_at and get_settings().enqueue_tasks:
        request_review.apply_async(args=[str(task.id)], eta=task.review_at)

    return CaptureTaskResponse(
        task=TaskResponse.model_validate(task, from_attributes=True),
        parsed=ParsedTask(**parsed.__dict__),
    )


@app.post("/plans/generate", response_model=PlanResponse)
def generate_plan(
    payload: GeneratePlanRequest,
    session: Session = Depends(get_session),
    provider: ModelProvider = Depends(get_model_provider),
) -> PlanResponse:
    task = session.exec(select(Task).where(Task.id == payload.task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    generated = provider.generate_plan(task)
    plan = Plan(
        task_id=task.id,
        summary=generated.summary,
        steps=generated.steps,
        token_estimate=generated.token_estimate,
        provider_name=generated.provider_name,
    )
    task.status = TaskStatus.planned
    session.add(task)
    session.add(plan)
    session.commit()
    session.refresh(plan)

    return PlanResponse.model_validate(plan, from_attributes=True)
