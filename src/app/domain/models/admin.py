import uuid
from typing import Optional

from sqlmodel import Field

from src.app.domain.schemas.user_base import UserBase


class Admin(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_code: uuid.UUID | None = Field(default_factory=uuid.uuid4, unique=True)
    password: str = Field(max_length=30, nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=True)
