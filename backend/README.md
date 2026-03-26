# Backend (FastAPI + MSSQL)

## Structure

```text
backend/
  app/
    core/
    db/
    models/
    routes/
    schemas/
    services/
    middleware/
  sql/mssql_schema.sql
```

## Setup

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Implemented

- JWT auth (`/api/v1/auth/login`)
- Lead create/list APIs (`/api/v1/leads`) with pagination/filtering + row-level behavior
- Reports APIs with joined aggregations:
  - `/api/v1/reports/sales-summary`
  - `/api/v1/reports/lead-pipeline`
- Placeholder routers for remaining modules (`users`, `deals`, `followups`, `products`, `quotations`, `orders`, `payments`, `visits`)
- SQL Server DDL script + join views in `sql/mssql_schema.sql`
