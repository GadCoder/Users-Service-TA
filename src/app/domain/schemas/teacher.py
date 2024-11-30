from src.app.domain.schemas.user_base import UserBase


class TeacherPublic(UserBase):
    id: int
    teacher_code: str
    is_active: bool


class TeacherCreate(UserBase):
    teacher_code: str
    password: str


class TeacherUpdate(UserBase):
    password: str
