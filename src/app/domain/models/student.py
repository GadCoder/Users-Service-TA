from sqlmodel import Field

from src.app.domain.schemas.user_base import UserBase


class Student(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_code: str = Field(max_length=8, unique=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
