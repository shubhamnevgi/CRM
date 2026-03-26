# Enterprise CRM + ERP

Production-oriented multi-tenant CRM + ERP scaffold using:
- **Frontend**: React (to be added in next phase)
- **Backend**: FastAPI
- **Database**: Microsoft SQL Server (SQLAlchemy + pyodbc)

## Implemented in this iteration

- Backend project structure
- Core configuration and DB session management
- Normalized MSSQL-ready data models for all requested tables
- JWT security utilities and RBAC dependency primitives
- Auth login endpoint and lead management endpoint with row-level filtering
- Placeholder API routers for all remaining modules
- Docker Compose for backend + MSSQL
- Seed script bootstrap

## Run with Docker

```bash
docker compose up --build
```

API: `http://localhost:8000`
