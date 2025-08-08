from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "alexhirsh@email.com",
                "password": "secret123"
            }
        }
    }


class RegisterRequest(BaseModel):
    login: str
    name: str
    surname: str
    second_name: Optional[str] = None
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "login": "john223",
                "name": "Alex",
                "surname": "Hirsh",
                "email": "alexhirsh@email.com",
                "password": "secret123"
            }
        }
    }


class TokenBase(BaseModel):
    token: str

    model_config = {
        "json_schema_extra": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkFsZXhIaXJzaEBlbWFpbC5jb20iLCJleHAiOjE3NTIzNTg4NTJ9.rtQAd9krUy-hKIjU5FBinf4QNDW7k3Tw7HwDy31yhYI"
        }
    }


class UserBase(BaseModel):
    user_id: str
    email: str
    is_admin: bool

    model_config = {
        "json_schema_extra": {
            "user_id": "6d101dad-4ed2-48e5-bf54-f2e0efdab389",
            "email": "alexhirsh@email.com",
            "is_admin": True
        }
    }