from uuid import UUID

from app.celery_app import celery_app


@celery_app.task(name="life_copilot.send_reminder")
def send_reminder(reminder_id: str) -> dict:
    return {"reminder_id": reminder_id, "status": "mocked"}


@celery_app.task(name="life_copilot.request_review")
def request_review(task_id: str) -> dict:
    UUID(task_id)
    return {"task_id": task_id, "status": "mocked"}

