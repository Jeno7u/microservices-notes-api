import httpx

from fastapi import Depends

from app.core.security.errors import InvalidAuthorizationTokenError


async def validate_token(token) -> dict:
    """
    Проверка jwt-токена в auth микросервисе
    В случае успеха возвращает {"email": email}
    """
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth:8000/auth/validate-token/", json={"token": token})

    response_data = response.json()

    # если возникли проблемы с токеном
    if response.status_code != 200 or "detail" in response_data:
        raise InvalidAuthorizationTokenError()

    return response_data

    