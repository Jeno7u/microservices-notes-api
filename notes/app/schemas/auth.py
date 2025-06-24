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