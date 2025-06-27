import jwt
import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.notes import CreateNoteRequest
from app.schemas.response import ResponseBase
from app.core.utils import validate_token


async def create_note_service(
        request_body: CreateNoteRequest, 
        session: AsyncSession, 
        token: str
    ) -> ResponseBase:
    data = {"token": token}
    reponse = await validate_token(data)
    
    return reponse
    