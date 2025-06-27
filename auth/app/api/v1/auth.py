from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.auth import login_service, register_service
from app.schemas.auth import LoginRequest, RegisterRequest
from app.core.security.utils import check_jwt


router = APIRouter()


@router.post("/login/")
async def login(request_body: LoginRequest, session: AsyncSession = Depends(get_db)):
    """
    Проверяет налиие пользователя с такими данными и возвращает jwt-токен
    """
    response = await login_service(request_body, session)
    
    return response


@router.post("/register/")
async def register(request_body: RegisterRequest, session: AsyncSession = Depends(get_db)):
    """
    Проверяет валидность данных, создает пользователя и возвращает jwt-токен
    """
    response = await register_service(request_body, session)

    return response


@router.post("/validate-token/")
async def validate_token(request_body: dict):
    """
    Проверка валидности jwt-токена
    """
    token = request_body["token"]
    response = await check_jwt(token)

    return response
    