import httpx
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


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
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                json=json_data,
                headers=headers
            )

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid authorization token")
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="No rights to access this note")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Note not found")
            elif response.status_code == 409:
                raise HTTPException(status_code=409, detail="Note with same name already exists")
            elif response.status_code == 422:
                raise HTTPException(status_code=422, detail="Validation error")
            elif response.status_code != expected_status:
                raise HTTPException(status_code=500, detail="Service unavailable")

            return response.json()
            

notes_client = ServiceClient("http://auth:8000")