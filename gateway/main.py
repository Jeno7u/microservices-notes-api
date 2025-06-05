# gateway/main.py
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        res = await client.post("http://auth:8001/login", json=data)
        return res.json()

@app.get("/profile")
async def profile(request: Request):
    token = request.headers.get("Authorization")
    async with httpx.AsyncClient() as client:
        res = await client.get("http://user:8002/profile", headers={"Authorization": token})
        return res.json()
