from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    names: str
    last_names: str
    email: str = Field(unique=True)
    picture_url: str | None
