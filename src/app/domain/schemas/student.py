from src.app.domain.schemas.user_base import UserBase


class StudentPublic(UserBase):
    id: int
    student_code: str
    is_active: bool
    picture_url: str | None


class StudentCreate(UserBase):
    picture_bytes: str
    student_code: str
