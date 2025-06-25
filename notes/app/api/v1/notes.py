from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.auth import login_service, register_service
from app.schemas.auth import LoginRequest, RegisterRequest


router = APIRouter()




@router.post("/create/")
async def login(request_body: LoginRequest, session: AsyncSession = Depends(get_db)):
    print(request_body)
    return {}


# creating note
# changing note
# deleting note
