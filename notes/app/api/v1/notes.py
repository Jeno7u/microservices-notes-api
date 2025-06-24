from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.auth import login_service, register_service
from app.schemas.auth import LoginRequest, RegisterRequest


router = APIRouter()


@router.post("/login/")
async def login(request_body: LoginRequest, session: AsyncSession = Depends(get_db)):
    print(request_body)
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