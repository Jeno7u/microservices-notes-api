# user/main.py
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/profile")
def profile(request: Request):
    auth = request.headers.get("Authorization")
    if auth != "valid_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": "admin", "bio": "I love FastAPI!"}
