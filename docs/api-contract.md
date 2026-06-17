# API Contract

## Base URL

Local development API base URL:

```text
http://localhost:8000
```

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## Capture Task

```http
POST /tasks/capture
```

Request:

```json
{
  "text": "今天整理报销材料，周五前完成"
}
```

Response includes:

- saved task
- parsed task
- mock provider name
- token estimate

## Generate Plan

```http
POST /plans/generate
```

Request:

```json
{
  "task_id": "<task-id>"
}
```

Response includes:

- saved plan id
- task id
- plan summary
- ordered next-action steps
- mock provider name
- token estimate
