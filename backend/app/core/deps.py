from collections.abc import Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.entities import Role, User
from app.models.enums import RoleName

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication token')

    user = db.scalar(select(User).where(User.id == int(user_id), User.is_active.is_(True)))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found or inactive')
    return user


def require_roles(allowed_roles: Iterable[RoleName]):
    allowed = set(allowed_roles)

    def _validator(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> User:
        role = db.scalar(select(Role).where(Role.id == current_user.role_id))
        if not role or role.name not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
        return current_user

    return _validator
