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

