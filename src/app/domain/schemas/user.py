from src.app.domain.schemas.user_base import UserBase
from sqlmodel import SQLModel, Field


class UserPublic(UserBase):
    id: int
    is_active: bool
    is_teacher: bool
    code: str


class UserCreate(UserBase):
    is_teacher: bool
    code: str
    password: str


class UserUpdatePicture(SQLModel):
    id: int
    picture_url: str


class UserUpdatePassword(SQLModel):
    id: int
    existing_password: str
    new_password: str


class UserUpdateActiveStatus(SQLModel):
    id: int
    is_active: bool


class UserDelete(SQLModel):
    pass
