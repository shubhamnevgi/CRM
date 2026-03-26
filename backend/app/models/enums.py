import enum


class RoleName(str, enum.Enum):
    ADMIN = 'Admin'
    SALES_MANAGER = 'Sales Manager'
    SALES_EXECUTIVE = 'Sales Executive'
    ACCOUNTANT = 'Accountant'


class LeadStatus(str, enum.Enum):
    NEW = 'New'
    CONTACTED = 'Contacted'
    QUALIFIED = 'Qualified'
    LOST = 'Lost'


class PipelineStage(str, enum.Enum):
    LEAD = 'Lead'
    QUALIFIED = 'Qualified'
    PROPOSAL = 'Proposal'
    NEGOTIATION = 'Negotiation'
    WON = 'Won'
    LOST = 'Lost'


class QuotationStatus(str, enum.Enum):
    DRAFT = 'Draft'
    SENT = 'Sent'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    CONVERTED = 'Converted'


class OrderStatus(str, enum.Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    FULFILLED = 'Fulfilled'
    CANCELLED = 'Cancelled'
