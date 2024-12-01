from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    names: str
    last_names: str
    email: EmailStr = Field(unique=True)
    picture_url: str | None


class UserLoginInput(SQLModel):
    email: EmailStr
    password: str


class UserLoginOutput(SQLModel):
    id: int
    user_name: str
    email: str
    is_active: bool
    is_super_user: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True
