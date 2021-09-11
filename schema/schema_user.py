from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str
