from fastapi import APIRouter, Request
import httpx

router = APIRouter()

@router.post("/register/")
async def register(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        res = await client.post("http://auth:8001/auth/register/", json=data)
        return res.json()

@router.post("/login/")
async def login(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        res = await client.post("http://auth:8001/auth/login/", json=data)
        print(res)
        return res.json()


