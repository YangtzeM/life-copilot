# life-copilot

Life Copilot MVP monorepo.

The MVP helps procrastination-prone users capture natural language tasks, parse priority, generate small next-action plans, schedule reminders, support review, and store basic memory.

## Repository Structure

```text
life-copilot/
  apps/
    mobile/              # React Native Expo App
    api/                 # FastAPI backend
  packages/
    shared/              # shared types and interface definitions
  docs/
    product-spec.md      # product spec
    architecture.md      # technical architecture
    api-contract.md      # API contract
    codex-tasks.md       # Codex task list
  docker-compose.yml
  README.md
```

## Local Startup

Start the backend, PostgreSQL, Redis, and Celery worker:

```powershell
docker compose up --build
```

API base URL:

```text
http://localhost:8000
```

Health check:

```powershell
curl http://localhost:8000/health
```

Capture a task:

```powershell
curl -X POST http://localhost:8000/tasks/capture `
  -H "Content-Type: application/json" `
  -d "{\"text\":\"Prepare reimbursement materials by Friday\"}"
```

Generate a plan with the returned `task.id`:

```powershell
curl -X POST http://localhost:8000/plans/generate `
  -H "Content-Type: application/json" `
  -d "{\"task_id\":\"<task-id>\"}"
```

## Backend Tests

```powershell
cd apps/api
python -m pip install -e ".[dev]"
pytest
```

The tests run against SQLite and disable Celery enqueueing so they do not require PostgreSQL or Redis.

## MVP Boundaries

This repository intentionally avoids multi-agent orchestration, LangGraph, vector databases, broad integrations, and autonomous external actions.
