from sqlmodel import SQLModel


class UserBase(SQLModel):
    names: str
    last_names: str
    email: str
    picture_url: str | None
