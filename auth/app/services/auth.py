import os 
import datetime
from typing import Dict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.exc import UnknownHashError

from app.schemas.auth import LoginRequest, RegisterRequest, TokenBase
from app.core.security.utils import authenticate_user, create_access_token, get_password_hash, check_jwt
from app.core.security.errors import IncorrectUserDataException, InvalidAuthorizationTokenError, UserNotFoundException
from app.models import User
from app.crud.user import get_user_by_email


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


async def login_service(lr: LoginRequest, session: AsyncSession) -> TokenBase:
    """
    Функция, которая проверяет есть ли такой пользователь и если есть, то подтягивает из базы его данные
    :param lr: LoginRequest
    :return: token
    """
    try:
        user = await authenticate_user(lr.email, lr.password, session)
    except (IncorrectUserDataException, UnknownHashError):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    email = lr.email
    token = create_access_token({"email": email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"token": token}


async def register_service(rr: RegisterRequest, session: AsyncSession) -> TokenBase:
    """
    Функция регистрации
    :param rr: request body
    :return: token
    """
    existing_user = await session.execute(select(User).where(User.email == rr.email))
    existing_user = existing_user.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с введенной почтой уже зарегистрирован!")
    # if frontend woudnt validate data we should do it there
    hashed_password = get_password_hash(rr.password)
    new_user = User(
        login=rr.login,
        name=rr.name,
        surname=rr.surname,
        second_name=rr.second_name,
        email=rr.email,
        password=hashed_password,
        is_admin=False,
    )              
    try:
        session.add(new_user)
        await session.commit()
        await session.close()
        token = create_access_token({"email": rr.email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"token": token}
    except Exception as e:
        session.rollback()
        session.close()
        raise e


async def validate_token_service(token: str, session: AsyncSession) -> dict:
    """
    Validate JWT token and return user information
    """
    try:
        token_data = await check_jwt(token)
        email = token_data.get("email")
        
        if not email:
            raise InvalidAuthorizationTokenError()
        
        user = await get_user_by_email(email, session)
        if not user:
            raise UserNotFoundException(email)
        
        return {
            "valid": True,
            "user_id": str(user.id),
            "email": user.email,
            "is_admin": user.is_admin
        }
        
    except (InvalidAuthorizationTokenError, UserNotFoundException) as e:
        raise e
    except Exception as e:
        raise InvalidAuthorizationTokenError()