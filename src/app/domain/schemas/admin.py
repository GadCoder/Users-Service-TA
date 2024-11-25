from src.app.domain.schemas.user_base import UserBase


class AdminPublic(UserBase):
    id: int


class AdminCreate(UserBase):
    password: str


class AdminUpdate(UserBase):
    password: str
