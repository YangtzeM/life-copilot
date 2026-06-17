from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskPriority(str, Enum):
    urgent = "urgent"
    important = "important"
    optional = "optional"
    low_value = "low_value"


class TaskStatus(str, Enum):
    captured = "captured"
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    reviewed = "reviewed"


class TaskBase(SQLModel):
    raw_text: str
    title: str
    description: str = ""
    priority: TaskPriority = TaskPriority.optional
    status: TaskStatus = TaskStatus.captured
    due_at: datetime | None = None
    reminder_at: datetime | None = None
    review_at: datetime | None = None
    user_context: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class PlanBase(SQLModel):
    task_id: UUID = Field(foreign_key="task.id", index=True)
    summary: str
    steps: list[dict] = Field(default_factory=list, sa_column=Column(JSON))
    token_estimate: int = 0
    provider_name: str = "mock"


class Plan(PlanBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)


class ReminderBase(SQLModel):
    task_id: UUID = Field(foreign_key="task.id", index=True)
    remind_at: datetime
    message: str
    delivered_at: datetime | None = None


class Reminder(ReminderBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)


class ReviewBase(SQLModel):
    task_id: UUID = Field(foreign_key="task.id", index=True)
    completed: bool
    what_worked: str = ""
    what_failed: str = ""
    next_adjustment: str = ""


class Review(ReviewBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)


class MemoryBase(SQLModel):
    key: str = Field(index=True)
    value: str
    source: str = "user"


class Memory(MemoryBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)
