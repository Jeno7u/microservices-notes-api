import jwt
import httpx

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.notes import CreateNoteRequest
from app.schemas.response import ResponseBase
from app.core.security.utils import validate_token
from app.core.security.errors import NoteWithSameNameAlreadyExistsError
from app.crud.note import get_note_by_name
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

    # проверка наличии заметки с таким же названием
    note_with_same_name = await get_note_by_name(session, response_validation["user_id"], request_body.name)

    if note_with_same_name != None:
        raise NoteWithSameNameAlreadyExistsError

    # надо будет сделать базоваое название для note
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


async def get_notes_service(session: AsyncSession, token: str):
    data = {"token": token}
    response_validation = await validate_token(data)

    # проверка валидности токена
    if "email" not in response_validation.keys():
        return response_validation
    
    notes = await session.execute(select(Note.name).where(Note.user_id == response_validation["user_id"]))
    notes_list = notes.scalars().all()

    await session.close()
    return {"notes": notes_list}
    
