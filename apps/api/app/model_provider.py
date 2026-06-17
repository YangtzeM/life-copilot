from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.models import Task, TaskPriority


@dataclass(frozen=True)
class ParsedTaskResult:
    title: str
    description: str
    priority: TaskPriority
    due_at: datetime | None
    reminder_at: datetime | None
    review_at: datetime | None
    smallest_next_action: str
    token_estimate: int
    provider_name: str


@dataclass(frozen=True)
class PlanResult:
    summary: str
    steps: list[dict]
    token_estimate: int
    provider_name: str


class ModelProvider(ABC):
    name: str

    @abstractmethod
    def parse_task(self, text: str) -> ParsedTaskResult:
        raise NotImplementedError

    @abstractmethod
    def generate_plan(self, task: Task) -> PlanResult:
        raise NotImplementedError


class MockModelProvider(ModelProvider):
    name = "mock"

    def parse_task(self, text: str) -> ParsedTaskResult:
        now = datetime.now(timezone.utc)
        normalized = " ".join(text.strip().split())
        priority = self._classify_priority(normalized)
        title = normalized[:80]
        reminder_at = now + timedelta(hours=1)
        review_at = now + timedelta(days=1)
        due_at = now + timedelta(days=2) if priority in {TaskPriority.urgent, TaskPriority.important} else None
        return ParsedTaskResult(
            title=title,
            description=f"Captured from user input: {normalized}",
            priority=priority,
            due_at=due_at,
            reminder_at=reminder_at,
            review_at=review_at,
            smallest_next_action="Spend 5 minutes clarifying the first concrete step.",
            token_estimate=max(1, len(normalized) // 4),
            provider_name=self.name,
        )

    def generate_plan(self, task: Task) -> PlanResult:
        steps = [
            {
                "order": 1,
                "title": "Clarify the outcome",
                "description": "Write one sentence describing what done means for this task.",
            },
            {
                "order": 2,
                "title": "Take the smallest next action",
                "description": "Spend 5 to 10 minutes on the easiest action that moves the task forward.",
            },
            {
                "order": 3,
                "title": "Review and adjust",
                "description": "Check what worked, what got stuck, and choose the next small step.",
            },
        ]
        return PlanResult(
            summary=f"Simple plan for: {task.title}",
            steps=steps,
            token_estimate=max(1, (len(task.raw_text) + len(task.title)) // 4),
            provider_name=self.name,
        )

    def _classify_priority(self, text: str) -> TaskPriority:
        lowered = text.lower()
        urgent_markers = ["urgent", "asap", "today", "tonight", "deadline", "马上", "今天", "紧急"]
        important_markers = ["important", "health", "exam", "report", "重要", "体检", "考试", "报销"]
        low_value_markers = ["maybe", "someday", "optional", "有空", "随便"]
        if any(marker in lowered for marker in urgent_markers):
            return TaskPriority.urgent
        if any(marker in lowered for marker in important_markers):
            return TaskPriority.important
        if any(marker in lowered for marker in low_value_markers):
            return TaskPriority.low_value
        return TaskPriority.optional


def get_model_provider() -> ModelProvider:
    return MockModelProvider()

