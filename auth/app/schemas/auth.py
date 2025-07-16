from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    login: str
    name: str
    surname: str
    second_name: str = None
    email: str
    password: str


class TokenBase(BaseModel):
    token: str = None


class UserBase(BaseModel):
    user_id: str
    email: str
    is_admin: bool