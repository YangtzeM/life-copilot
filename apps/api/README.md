# life-copilot API

FastAPI backend for the Life Copilot MVP.

## Local Development

Install dependencies:

```powershell
cd apps/api
python -m pip install -e ".[dev]"
```

Run the API against local services:

```powershell
uvicorn app.main:app --reload
```

Run tests:

```powershell
pytest
```

## API

- `GET /health`
- `POST /tasks/capture`
- `POST /plans/generate`

All model behavior is currently served by the mock `ModelProvider`.
