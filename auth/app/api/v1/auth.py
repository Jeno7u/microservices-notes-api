from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.app.core.db import get_db
from auth.app.services.auth import login_service, register_service, validate_token_service
from auth.app.schemas.auth import LoginRequest, RegisterRequest, TokenBase, UserBase, AuthorizationResponse
from auth.app.schemas.response import ErrorResponse


router = APIRouter()

@router.post("/login/",
             status_code=status.HTTP_200_OK,
             response_model=AuthorizationResponse,
             responses={
                 401: {"model": ErrorResponse, "description": "Incorrect email or password"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
            })
async def login(request_body: LoginRequest, session: AsyncSession = Depends(get_db)):
    """Checks user existance and returns jwt token"""
    response = await login_service(request_body, session)
    
    return response


@router.post("/register/",
             status_code=status.HTTP_201_CREATED,
             response_model=AuthorizationResponse,
             responses={
                 409: {"model": ErrorResponse, "description": "User with that email already exists"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
            })
async def register(request_body: RegisterRequest, session: AsyncSession = Depends(get_db)):
    """Validates input data, creates user based on that and returns jwt token"""
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
    """Validates jwt token and returns some user data"""
    response = await validate_token_service(request_body.token, session)

    return response
    