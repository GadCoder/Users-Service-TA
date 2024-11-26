from sqlmodel import Field

from src.app.domain.schemas.user_base import UserBase


class Teacher(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    teacher_code: str = Field(max_length=6, nullable=False, unique=True)
    password: str = Field(max_length=30, nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
