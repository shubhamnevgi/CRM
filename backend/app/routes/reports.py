from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Deal, Lead, Order, Payment, User
from app.models.enums import LeadStatus, PipelineStage

router = APIRouter(prefix='/reports', tags=['Reports'])


@router.get('/sales-summary')
def sales_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    from_date: date | None = Query(default=None),
    to_date: date | None = Query(default=None),
):
    stmt = (
        select(
            func.count(Order.id).label('orders_count'),
            func.coalesce(func.sum(Order.total_amount), 0).label('booked_revenue'),
            func.coalesce(func.sum(Payment.amount), 0).label('received_amount'),
        )
        .outerjoin(Payment, Payment.order_id == Order.id)
        .where(Order.company_id == current_user.company_id)
    )

    if from_date:
        stmt = stmt.where(Order.order_date >= from_date)
    if to_date:
        stmt = stmt.where(Order.order_date <= to_date)

    result = db.execute(stmt).mappings().one()
    return dict(result)


@router.get('/lead-pipeline')
def lead_pipeline(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = (
        select(
            Deal.stage,
            func.count(Deal.id).label('deal_count'),
            func.coalesce(func.sum(Deal.value), 0).label('total_value'),
        )
        .where(Deal.company_id == current_user.company_id)
        .group_by(Deal.stage)
    )

    grouped = {stage.value: {'deal_count': 0, 'total_value': 0} for stage in PipelineStage}
    for row in db.execute(stmt):
        grouped[row.stage.value] = {'deal_count': row.deal_count, 'total_value': float(row.total_value)}

    conversion_stmt = (
        select(
            func.count(Lead.id).label('total_leads'),
            func.sum(case((Lead.status == LeadStatus.QUALIFIED, 1), else_=0)).label('qualified_leads'),
        )
        .where(Lead.company_id == current_user.company_id)
    )
    conversion = db.execute(conversion_stmt).mappings().one()
    total = conversion['total_leads'] or 0
    qualified = conversion['qualified_leads'] or 0
    conversion_rate = (qualified / total * 100) if total else 0

    return {'pipeline': grouped, 'lead_conversion_rate': round(conversion_rate, 2)}
