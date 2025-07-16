from datetime import datetime, timezone, timedelta
from typing import Union, Annotated
import os

import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from passlib.context import CryptContext

from app.models import User
from app.crud.user import get_user_by_email
from app.core.security.errors import (
    IncorrectUserDataException,
    InvalidAuthorizationTokenError,
)

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return str(hashed_password)


async def authenticate_user(email: str, password: str, session: AsyncSession) -> User:
    user = await get_user_by_email(email, session)

    if not user or not verify_password(password, user.password):
        raise IncorrectUserDataException()
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        expire = datetime.fromtimestamp(int(payload.get("exp")))
        if datetime.now() > expire or email is None:
            raise InvalidAuthorizationTokenError()
    except jwt.InvalidTokenError:
        raise InvalidAuthorizationTokenError()
    return {"email": email}
