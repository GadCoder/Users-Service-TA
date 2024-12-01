import uuid

from src.app.domain.schemas.user_base import UserBase


class AdminPublic(UserBase):
    is_superuser: bool
    is_active: bool
    admin_code: uuid.UUID
    id: int


class AdminCreate(UserBase):
    password: str


class AdminUpdate(UserBase):
    password: str
