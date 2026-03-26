from pydantic import EmailStr

from app.schemas.common import ORMBaseModel, TenantAuditBase, TenantAuditRead


class UserCreate(TenantAuditBase):
    role_id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    password: str


class UserRead(ORMBaseModel, TenantAuditRead):
    id: int
    role_id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    is_active: bool
