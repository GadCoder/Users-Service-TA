from sqlmodel import SQLModel


class UserBase(SQLModel):
    names: str
    last_names: str
    email: str
    picture_url: str | None
    is_active: bool = True
    is_superuser: bool = False
