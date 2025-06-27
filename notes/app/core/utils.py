import httpx

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


def get_current_token(authorization: HTTPAuthorizationCredentials = Depends(security)):
    return authorization.credentials

async def validate_token(data) -> bool:
    async with httpx.AsyncClient() as client:
        res = await client.post("http://auth:8000/auth/validate-token/", json=data)
        return res.json()
        