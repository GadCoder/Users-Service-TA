from src.app.domain.schemas.user_base import UserBase


class StudentPublic(UserBase):
    id: int
    student_code: str
    is_active: bool


class StudentCreate(UserBase):
    student_code: str
