from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Lead, Role, User
from app.models.enums import LeadStatus, RoleName
from app.schemas.lead import LeadCreate, LeadRead

router = APIRouter(prefix='/leads', tags=['Leads'])


@router.post('', response_model=LeadRead)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lead = Lead(**payload.model_dump(), created_by=current_user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get('', response_model=list[LeadRead])
def list_leads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: LeadStatus | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=200),
):
    stmt = select(Lead).where(Lead.company_id == current_user.company_id)

    if status:
        stmt = stmt.where(Lead.status == status)

    # Row-level restriction: non-admin and non-sales-manager users only see assigned leads.
    role = db.scalar(select(Role).where(Role.id == current_user.role_id))
    if role and role.name not in {RoleName.ADMIN, RoleName.SALES_MANAGER}:
        stmt = stmt.where(Lead.assigned_user_id == current_user.id)

    leads = db.scalars(stmt.offset(skip).limit(limit)).all()
    return list(leads)
