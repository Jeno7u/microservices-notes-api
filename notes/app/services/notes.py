import jwt
import httpx

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.notes import CreateNoteRequest
from app.schemas.response import ResponseBase
from app.core.security.utils import validate_token
from app.models import Note


async def create_note_service(
        request_body: CreateNoteRequest, 
        session: AsyncSession, 
        token: str
    ) -> ResponseBase:
    data = {"token": token}
    response_validation = await validate_token(data)

    # проверка валидности токена
    if "email" not in response_validation.keys():
        return response_validation
    
    # validation is user still in db
    """
    existing_user = await session.execute(select(User).where(User.email == email))
    existing_user = existing_user.scalars().first()

    if not existing_user:
        return
    """
    
    new_note = Note(
        name=request_body.name,
        text=request_body.text,
        user_id=response_validation["user_id"]
    )
    try:
        session.add(new_note)
        await session.commit()
        await session.close()
        return {"status_code": 200}
    except Exception as e:
        await session.rollback()
        await session.close()
        raise e
