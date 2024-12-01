from typing import Optional

from sqlmodel import Field

from src.app.domain.schemas.user_base import UserBase


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=20, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    is_teacher: bool = Field(default=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
