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
```

## Quick start

1. Copy env:
   ```bash
   cp .env.example .env
   ```
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Run API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Scope completed in this phase

- FastAPI bootstrap and config
- MSSQL SQLAlchemy database wiring
- Normalized multi-tenant models with required audit columns
- Initial auth + lead APIs with JWT auth and row-level lead filtering
- Endpoint scaffolds for remaining modules
- Docker compose for backend + MSSQL

## Next phase

- Complete CRUD/services for all modules
- Add Alembic migration scripts
- Add React frontend and integrate all APIs
