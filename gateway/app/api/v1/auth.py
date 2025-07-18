import httpx
from fastapi import APIRouter, status, Depends, HTTPException

from app.schemas.response import ErrorResponse
from app.schemas.auth import LoginRequest, RegisterRequest, TokenBase, UserBase


router = APIRouter()

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def make_request(
        self,
        method: str,
        endpoint: str,
        json_data=None,
        headers=None,
        expected_status=200
    ):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=f"{self.base_url}{endpoint}",
                    json=json_data,
                    headers=headers
                )

                if response.status_code == expected_status:
                    return response.json()
                
                try:
                    error_data = response.json()
                    detail = error_data.get("detail", "Service error")
                except:
                    detail = "Service error"

                raise HTTPException(status_code=response.status_code, detail=detail)
        
        except HTTPException:
            raise
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Auth service timeout")
        except Exception:
            raise HTTPException(status_code=503, detail="Auth service unavailable")
            

auth_client = ServiceClient("http://auth:8000")


@router.post("/login/",
             status_code=status.HTTP_200_OK,
             response_model=TokenBase,
             responses={
                 401: {"model": ErrorResponse, "description": "Incorrect email or password"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"},
                 503: {"model": ErrorResponse, "description": "Auth service unavailable"},
                 504: {"model": ErrorResponse, "description": "Auth service timeout"}
            })
async def login(request_body: LoginRequest):
    """
    Проверяет налиие пользователя с такими данными и возвращает jwt-токен
    """
    response = await auth_client.make_request(
        method="post",
        endpoint="/auth/login/",
        json_data=request_body.model_dump(),
        expected_status=200
    )

    return response


@router.post("/register/",
             status_code=status.HTTP_201_CREATED,
             response_model=TokenBase,
             responses={
                 409: {"model": ErrorResponse, "description": "User with that email already exists"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"},
                 503: {"model": ErrorResponse, "description": "Auth service unavailable"},
                 504: {"model": ErrorResponse, "description": "Auth service timeout"}
            })
async def register(request_body: RegisterRequest):
    """
    Проверяет валидность данных, создает пользователя и возвращает jwt-токен
    """
    response = await auth_client.make_request(
        method="post",
        endpoint="/auth/register/",
        json_data=request_body.model_dump(),
        expected_status=201
    )

    return response


@router.post("/validate-token/",
             status_code=status.HTTP_200_OK,
             response_model=UserBase,
             responses={
                 401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                 404: {"model": ErrorResponse, "description": "User not found"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"},
                 503: {"model": ErrorResponse, "description": "Auth service unavailable"},
                 504: {"model": ErrorResponse, "description": "Auth service timeout"}
            })
async def validate_token(request_body: TokenBase):
    """
    Проверка валидности jwt-токена и получения данных пользователя
    """
    response = await auth_client.make_request(
        method="post",
        endpoint="/auth/validate-token/",
        json_data=request_body.model_dump(),
        expected_status=200
    )

    return response