-- Enterprise CRM + ERP (MSSQL) normalized schema
-- This script is useful when provisioning DB directly in SQL Server.

CREATE TABLE companies (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(200) NOT NULL UNIQUE,
    is_active BIT NOT NULL DEFAULT 1
);

CREATE TABLE branches (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    name NVARCHAR(200) NOT NULL,
    address NVARCHAR(500) NULL,
    CONSTRAINT FK_branches_companies FOREIGN KEY (company_id) REFERENCES companies(id)
);
CREATE INDEX IX_branches_company_name ON branches(company_id, name);

CREATE TABLE departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    name NVARCHAR(200) NOT NULL,
    CONSTRAINT FK_departments_companies FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_departments_branches FOREIGN KEY (branch_id) REFERENCES branches(id)
);
CREATE INDEX IX_departments_scope_name ON departments(company_id, branch_id, name);

CREATE TABLE roles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL UNIQUE,
    description NVARCHAR(255) NULL
);

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    role_id INT NOT NULL,
    full_name NVARCHAR(200) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE,
    phone NVARCHAR(30) NULL,
    password_hash NVARCHAR(255) NOT NULL,
    is_active BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_users_companies FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_users_branches FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_users_departments FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_users_roles FOREIGN KEY (role_id) REFERENCES roles(id),
    CONSTRAINT FK_users_created_by FOREIGN KEY (created_by) REFERENCES users(id)
);
CREATE INDEX IX_users_company_role ON users(company_id, role_id);

CREATE TABLE leads (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    assigned_user_id INT NULL,
    customer_name NVARCHAR(200) NOT NULL,
    email NVARCHAR(255) NULL,
    phone NVARCHAR(30) NULL,
    source NVARCHAR(100) NULL,
    status NVARCHAR(30) NOT NULL,
    address NVARCHAR(500) NULL,
    notes NVARCHAR(MAX) NULL,
    CONSTRAINT FK_leads_companies FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_leads_branches FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_leads_departments FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_leads_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT FK_leads_assigned_user FOREIGN KEY (assigned_user_id) REFERENCES users(id)
);
CREATE INDEX IX_leads_company_status ON leads(company_id, status);
CREATE INDEX IX_leads_assigned_status ON leads(assigned_user_id, status);


CREATE TABLE deals (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    lead_id INT NOT NULL,
    owner_user_id INT NOT NULL,
    stage NVARCHAR(30) NOT NULL,
    value DECIMAL(18,2) NOT NULL,
    probability INT NOT NULL,
    expected_close_date DATE NULL,
    CONSTRAINT FK_deals_company FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_deals_branch FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_deals_department FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_deals_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT FK_deals_lead FOREIGN KEY (lead_id) REFERENCES leads(id),
    CONSTRAINT FK_deals_owner FOREIGN KEY (owner_user_id) REFERENCES users(id)
);

CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    sku NVARCHAR(64) NOT NULL,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    gst_percent DECIMAL(5,2) NOT NULL DEFAULT 0,
    stock_quantity DECIMAL(18,2) NOT NULL DEFAULT 0,
    is_active BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_products_company FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_products_branch FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_products_department FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_products_created_by FOREIGN KEY (created_by) REFERENCES users(id)
);
CREATE UNIQUE INDEX IX_products_tenant_sku ON products(company_id, branch_id, department_id, sku);

CREATE TABLE quotations (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    lead_id INT NULL,
    deal_id INT NULL,
    quotation_number NVARCHAR(100) NOT NULL,
    valid_until DATE NULL,
    subtotal DECIMAL(18,2) NOT NULL DEFAULT 0,
    tax_total DECIMAL(18,2) NOT NULL DEFAULT 0,
    grand_total DECIMAL(18,2) NOT NULL DEFAULT 0,
    status NVARCHAR(30) NOT NULL,
    CONSTRAINT FK_quotations_company FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_quotations_branch FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_quotations_department FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_quotations_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT FK_quotations_lead FOREIGN KEY (lead_id) REFERENCES leads(id),
    CONSTRAINT FK_quotations_deal FOREIGN KEY (deal_id) REFERENCES deals(id)
);

CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    quotation_id INT NOT NULL,
    order_number NVARCHAR(100) NOT NULL,
    status NVARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(18,2) NOT NULL,
    CONSTRAINT FK_orders_company FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_orders_branch FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_orders_department FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_orders_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT FK_orders_quotation FOREIGN KEY (quotation_id) REFERENCES quotations(id)
);

CREATE TABLE payments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id INT NOT NULL,
    branch_id INT NOT NULL,
    department_id INT NOT NULL,
    created_by INT NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    order_id INT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_mode NVARCHAR(50) NOT NULL,
    reference_number NVARCHAR(150) NULL,
    notes NVARCHAR(MAX) NULL,
    CONSTRAINT FK_payments_company FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT FK_payments_branch FOREIGN KEY (branch_id) REFERENCES branches(id),
    CONSTRAINT FK_payments_department FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT FK_payments_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT FK_payments_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Joins / reporting views
CREATE VIEW vw_lead_owner AS
SELECT
    l.id AS lead_id,
    l.customer_name,
    l.status,
    l.created_at,
    u.id AS owner_id,
    u.full_name AS owner_name,
    d.name AS department_name,
    b.name AS branch_name,
    c.name AS company_name
FROM leads l
LEFT JOIN users u ON u.id = l.assigned_user_id
INNER JOIN departments d ON d.id = l.department_id
INNER JOIN branches b ON b.id = l.branch_id
INNER JOIN companies c ON c.id = l.company_id;

CREATE VIEW vw_revenue_collection AS
SELECT
    o.company_id,
    o.branch_id,
    SUM(o.total_amount) AS booked_amount,
    SUM(ISNULL(p.amount, 0)) AS collected_amount,
    SUM(o.total_amount) - SUM(ISNULL(p.amount, 0)) AS outstanding_amount
FROM orders o
LEFT JOIN payments p ON p.order_id = o.id
GROUP BY o.company_id, o.branch_id;
