import httpx

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security.errors import InvalidAuthorizationTokenError, 


security = HTTPBearer()


def get_current_token(authorization: HTTPAuthorizationCredentials = Depends(security)):
    return authorization.credentials

async def validate_token(data) -> dict:
    """
    Проверка jwt-токена в auth микросервисе
    В случае успеха возвращает {"email": email}
    """
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth:8000/auth/validate-token/", json=data)

    response_data = response.json()

    # если возникли проблемы с токеном
    if response.status_code != 200 or "detail" in response_data:
        raise InvalidAuthorizationTokenError()

    return response_data

    