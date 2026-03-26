from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class TenantAuditMixin:
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=False, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False, index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'), nullable=False, index=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class IDMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
