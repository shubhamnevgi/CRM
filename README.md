# Enterprise CRM + ERP

Multi-tenant CRM + ERP scaffold with:
- **Backend**: FastAPI + SQLAlchemy + MSSQL (pyodbc)
- **Frontend**: React + Vite + Axios
- **Auth**: JWT + bcrypt

## Repository structure

```text
backend/
frontend/
docker-compose.yml
```

## Backend highlights

- Modular FastAPI app structure (`core`, `db`, `models`, `schemas`, `routes`, `services`, `middleware`)
- Multi-tenant models for CRM/ERP entities with tenant/audit columns
- JWT auth, RBAC dependencies, row-level lead access behavior
- Reporting join APIs (`/reports/sales-summary`, `/reports/lead-pipeline`)
- SQL Server schema script with joins/views at `backend/sql/mssql_schema.sql`

## Frontend highlights

- Login page
- Dashboard KPI view
- Leads management form + list
- Pipeline (kanban style summary)
- Quotation and Order module scaffolds
- Map-based visit tracking page (Google Maps embed placeholder)

## Run backend + MSSQL via Docker

```bash
docker compose up --build
```

## Run frontend locally

```bash
cd frontend
npm install
npm run dev
```

API base URL can be configured with `VITE_API_URL`.
