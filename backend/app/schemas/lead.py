from app.models.enums import LeadStatus
from app.schemas.common import ORMBaseModel, TenantAuditBase, TenantAuditRead


class LeadCreate(TenantAuditBase):
    assigned_user_id: int | None = None
    customer_name: str
    email: str | None = None
    phone: str | None = None
    source: str | None = None
    status: LeadStatus = LeadStatus.NEW
    address: str | None = None
    notes: str | None = None


class LeadRead(ORMBaseModel, TenantAuditRead):
    id: int
    assigned_user_id: int | None
    customer_name: str
    email: str | None
    phone: str | None
    source: str | None
    status: LeadStatus
    address: str | None
    notes: str | None
