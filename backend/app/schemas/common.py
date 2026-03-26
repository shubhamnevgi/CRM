from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TenantAuditBase(BaseModel):
    company_id: int
    branch_id: int
    department_id: int


class TenantAuditRead(TenantAuditBase):
    created_by: int | None
    created_at: datetime
