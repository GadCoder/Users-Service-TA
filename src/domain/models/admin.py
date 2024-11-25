from sqlmodel import Field

from src.domain.schemas.user_base import UserBase


class Admin(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field(max_length=30, nullable=False)
    is_superuser: bool = False
