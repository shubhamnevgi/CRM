from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import IDMixin, TenantAuditMixin
from app.models.enums import LeadStatus, OrderStatus, PipelineStage, QuotationStatus, RoleName


class Role(Base, IDMixin):
    __tablename__ = 'roles'

    name: Mapped[RoleName] = mapped_column(Enum(RoleName), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))


class Company(Base, IDMixin):
    __tablename__ = 'companies'

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Branch(Base, IDMixin):
    __tablename__ = 'branches'

    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500))

    __table_args__ = (Index('ix_branch_company_name', 'company_id', 'name'),)


class Department(Base, IDMixin):
    __tablename__ = 'departments'

    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=False, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    __table_args__ = (Index('ix_department_scope_name', 'company_id', 'branch_id', 'name'),)


class User(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'users'

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Lead(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'leads'

    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), index=True)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(30), index=True)
    source: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(String(500))
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (Index('ix_leads_assignment_status', 'assigned_user_id', 'status'),)


class Deal(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'deals'

    lead_id: Mapped[int] = mapped_column(ForeignKey('leads.id'), nullable=False, index=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    stage: Mapped[PipelineStage] = mapped_column(Enum(PipelineStage), nullable=False, index=True)
    value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    probability: Mapped[int] = mapped_column(nullable=False)
    expected_close_date: Mapped[date | None] = mapped_column(Date)


class FollowUp(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'followups'

    lead_id: Mapped[int | None] = mapped_column(ForeignKey('leads.id'), index=True)
    deal_id: Mapped[int | None] = mapped_column(ForeignKey('deals.id'), index=True)
    assigned_to_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    next_follow_up_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Product(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'products'

    sku: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    gst_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    stock_quantity: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (Index('ix_products_tenant_sku', 'company_id', 'branch_id', 'department_id', 'sku', unique=True),)


class Quotation(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'quotations'

    lead_id: Mapped[int | None] = mapped_column(ForeignKey('leads.id'), index=True)
    deal_id: Mapped[int | None] = mapped_column(ForeignKey('deals.id'), index=True)
    quotation_number: Mapped[str] = mapped_column(String(100), nullable=False)
    valid_until: Mapped[date | None] = mapped_column(Date)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    tax_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    grand_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    status: Mapped[QuotationStatus] = mapped_column(Enum(QuotationStatus), default=QuotationStatus.DRAFT, nullable=False)

    items: Mapped[list['QuotationItem']] = relationship(back_populates='quotation', cascade='all, delete-orphan')


class QuotationItem(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'quotation_items'

    quotation_id: Mapped[int] = mapped_column(ForeignKey('quotations.id'), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False, index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    gst_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    quotation: Mapped['Quotation'] = relationship(back_populates='items')


class Order(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'orders'

    quotation_id: Mapped[int] = mapped_column(ForeignKey('quotations.id'), nullable=False, index=True)
    order_number: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)


class Payment(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'payments'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_number: Mapped[str | None] = mapped_column(String(150))
    notes: Mapped[str | None] = mapped_column(Text)


class Visit(Base, IDMixin, TenantAuditMixin):
    __tablename__ = 'visits'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    customer_lead_id: Mapped[int | None] = mapped_column(ForeignKey('leads.id'), index=True)
    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    visited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
