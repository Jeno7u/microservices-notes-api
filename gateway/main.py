from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/register")
async def login(request: Request):
    data = await request.json()
    print(data)
    async with httpx.AsyncClient() as client:
        res = await client.post("http://auth:8000/auth/register", json=data)
        print(res.status_code)
        print(res.headers.get("content-type"))
        print(res.text)
        return res.json()

# @app.get("/profile")
# async def profile(request: Request):
#     token = request.headers.get("Authorization")
#     async with httpx.AsyncClient() as client:
#         res = await client.get("http://user:8002/profile", headers={"Authorization": token})
#         return res.json()
