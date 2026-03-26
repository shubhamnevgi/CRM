"""Basic seed script for roles and an admin user."""

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.entities import Company, Branch, Department, Role, User
from app.models.enums import RoleName


def run_seed() -> None:
    db = SessionLocal()
    try:
        existing_roles = {r.name for r in db.scalars(select(Role)).all()}
        for role_name in RoleName:
            if role_name not in existing_roles:
                db.add(Role(name=role_name, description=f'{role_name.value} role'))

        company = db.scalar(select(Company).where(Company.name == 'Default Company'))
        if not company:
            company = Company(name='Default Company')
            db.add(company)
            db.flush()

        branch = db.scalar(select(Branch).where(Branch.name == 'HQ', Branch.company_id == company.id))
        if not branch:
            branch = Branch(name='HQ', company_id=company.id, address='Head Office')
            db.add(branch)
            db.flush()

        department = db.scalar(
            select(Department).where(
                Department.name == 'Sales',
                Department.company_id == company.id,
                Department.branch_id == branch.id,
            )
        )
        if not department:
            department = Department(name='Sales', company_id=company.id, branch_id=branch.id)
            db.add(department)
            db.flush()

        admin_role = db.scalar(select(Role).where(Role.name == RoleName.ADMIN))
        admin = db.scalar(select(User).where(User.email == 'admin@example.com'))
        if not admin and admin_role:
            db.add(
                User(
                    full_name='System Admin',
                    email='admin@example.com',
                    phone='0000000000',
                    password_hash=hash_password('Admin@123'),
                    role_id=admin_role.id,
                    company_id=company.id,
                    branch_id=branch.id,
                    department_id=department.id,
                    created_by=None,
                )
            )

        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    run_seed()
