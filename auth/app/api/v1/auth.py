from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.auth import login_service, register_service, validate_token_service
from app.schemas.auth import LoginRequest, RegisterRequest, TokenBase, UserBase
from app.schemas.response import ErrorResponse


router = APIRouter()

@router.post("/login/",
             status_code=status.HTTP_200_OK,
             response_model=TokenBase,
             responses={
                 401: {"model": ErrorResponse, "description": "Incorrect email or password"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
            })
async def login(request_body: LoginRequest, session: AsyncSession = Depends(get_db)):
    """
    Проверяет налиие пользователя с такими данными и возвращает jwt-токен
    """
    response = await login_service(request_body, session)
    
    return response


@router.post("/register/",
             status_code=status.HTTP_201_CREATED,
             response_model=TokenBase,
             responses={
                 409: {"model": ErrorResponse, "description": "User with that email already exists"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
            })
async def register(request_body: RegisterRequest, session: AsyncSession = Depends(get_db)):
    """
    Проверяет валидность данных, создает пользователя и возвращает jwt-токен
    """
    response = await register_service(request_body, session)

    return response


@router.post("/validate-token/",
             status_code=status.HTTP_200_OK,
             response_model=UserBase,
             responses={
                 401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                 404: {"model": ErrorResponse, "description": "User not found"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
            })
async def validate_token(request_body: TokenBase, session: AsyncSession = Depends(get_db)):
    """
    Проверка валидности jwt-токена и получения данных пользователя
    """
    response = await validate_token_service(request_body.token, session)

    return response
    