from collections.abc import Generator
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

os.environ["LIFE_DATABASE_URL"] = "sqlite://"
os.environ["LIFE_ENQUEUE_TASKS"] = "false"

from app.db import get_session  # noqa: E402
from app.main import app  # noqa: E402
from app.models import TaskPriority


@pytest.fixture(name="client")
def client_fixture() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_capture_task_and_generate_plan(client: TestClient) -> None:
    capture = client.post("/tasks/capture", json={"text": "今天整理报销材料，周五前完成"})
    assert capture.status_code == 200
    payload = capture.json()
    assert payload["task"]["title"] == "今天整理报销材料，周五前完成"
    assert payload["task"]["priority"] == TaskPriority.urgent.value
    assert payload["parsed"]["provider_name"] == "mock"

    plan = client.post("/plans/generate", json={"task_id": payload["task"]["id"]})
    assert plan.status_code == 200
    plan_payload = plan.json()
    assert plan_payload["task_id"] == payload["task"]["id"]
    assert len(plan_payload["steps"]) == 3
    assert plan_payload["provider_name"] == "mock"
