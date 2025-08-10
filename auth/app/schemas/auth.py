import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


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
    login: str = Field(..., min_length=3, max_length=25)
    name: str = Field(..., min_length=1, max_length=50)
    surname: str = Field(..., min_length=1, max_length=70)
    second_name: Optional[str] = Field(None, min_length=1, max_length=40)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("login")
    def validate_login(cls, v: str):
        """Login can only contain letters, numbers, and underscores"""
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Login can only contain letters, numbers, and underscores")
        if v.lower() in ["admin", "root", "user", "test"]:
            raise ValueError("This login is reserved")
        return v.lower()
    
    @field_validator("name", "surname", "second_name")
    def validate_name(cls, v: str):
        """Name/Surname/Second name should contain only letters and dashes"""
        if not re.match(r"^[a-zA-Z0-9-]+$", v):
            raise ValueError("Name/Surname/Second name can only contain letters, numbers, and underscores")
        if not re.match(r"--", v):
            raise ValueError("Name/Surname/Second name cannot have multiple dashes in a row")
        return v.capitalize()
    
    @field_validator("password")
    def validate_password(cls, v : str):
        """Password must contain at least one letter and one number"""
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number")
        return v

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