import os 
import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.auth import LoginRequest, RegisterRequest, TokenBase, UserBase
from app.core.security.utils import authenticate_user, create_access_token, get_password_hash, check_jwt
from app.core.security.errors import InvalidAuthorizationTokenError, UserNotFoundException, IncorrectUserDataException, InternalServerError
from app.models import User
from app.crud.user import get_user_by_email


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


async def login_service(request_body: LoginRequest, session: AsyncSession) -> TokenBase:
    """Service function that authenticates user and returns jwt token"""
    try:
        user = await authenticate_user(request_body.email, request_body.password, session)

        email = request_body.email
        token = create_access_token({"email": email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return TokenBase(token=token)
    
    except IncorrectUserDataException:
        raise
    except Exception:
        raise InternalServerError()
    finally:
        await session.close()


async def register_service(request_body: RegisterRequest, session: AsyncSession) -> TokenBase:
    """Service function for registration"""
    try:
        existing_user = await session.execute(select(User).where(User.email == request_body.email))
        existing_user = existing_user.scalars().first()

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

        token = create_access_token({"email": request_body.email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
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
        email = token_data.get("email")
        
        if not email:
            raise InvalidAuthorizationTokenError()
        
        user = await get_user_by_email(email, session)
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
        print(e)
        raise InternalServerError()
    finally:
        await session.close()