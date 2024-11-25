from src.domain.schemas.user_base import UserBase


class StudentPublic(UserBase):
    id: int
    student_code: str


class StudentCreate(UserBase):
    student_code: str
