import os 
import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.app.schemas.auth import LoginRequest, RegisterRequest, TokenBase, UserBase
from auth.app.core.security.utils import authenticate_user, create_access_token, get_password_hash, check_jwt
from auth.app.core.security.errors import InvalidAuthorizationTokenError, UserNotFoundException, IncorrectUserDataException, InternalServerError
from auth.app.models import User
from auth.app.crud.user import get_user_by_email, get_user_by_login


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


async def login_service(request_body: LoginRequest, session: AsyncSession) -> TokenBase:
    """Service function that authenticates user and returns jwt token"""
    try:
        user = await authenticate_user(request_body.login, request_body.password, session)

        login = request_body.login
        token = create_access_token({"login": login}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return TokenBase(token=token)
    
    except IncorrectUserDataException:
        raise
    except Exception as e:
        raise e
    finally:
        await session.close()


async def register_service(request_body: RegisterRequest, session: AsyncSession) -> TokenBase:
    """Service function for registration"""
    try:
        if "@" in request_body.login:
            existing_user = await get_user_by_email(request_body.login, session)
        else:
            existing_user = await get_user_by_login(request_body.login, session)

        if existing_user:
            raise HTTPException(status_code=409, detail="User with that email already exists")
        
        hashed_password = get_password_hash(request_body.password)
        new_user = User(
            login=request_body.login,
            name=request_body.name,
            surname=request_body.surname,
            second_name=request_body.second_name,
            email=request_body.email,
            password=hashed_password,
            is_admin=False,
        )              

        session.add(new_user)
        await session.commit()

        token = create_access_token({"login": request_body.email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return TokenBase(token=token)
    
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise InternalServerError()
    finally:
        await session.close()


async def validate_token_service(token: str, session: AsyncSession) -> UserBase:
    """Service function for token validation and returns basic user information"""
    try:
        token_data = await check_jwt(token)
        login = token_data.get("login")
        
        if not login:
            raise InvalidAuthorizationTokenError()
        
        if "@" in login:
            user = await get_user_by_email(login, session)
        else:
            user = await get_user_by_login(login, session)
            
        if not user:
            raise UserNotFoundException()
        
        return UserBase(
            user_id = str(user.id),
            email = user.email,
            is_admin = user.is_admin
        )
    except (InvalidAuthorizationTokenError, UserNotFoundException):
        raise
    except Exception as e:
        raise InternalServerError()
    finally:
        await session.close()