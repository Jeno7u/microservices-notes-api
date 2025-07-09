import jwt
import httpx

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.notes import CreateNoteRequest, UpdateNoteRequest
from app.schemas.response import ResponseBase
from app.core.security.utils import validate_token
from app.core.security.errors import NoteAlreadyExistsError, NoteNotFound
from app.crud.note import get_note_by_user_and_name, get_note_by_id, create_note
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
    note_with_same_name = await get_note_by_user_and_name(session, response_validation["user_id"], request_body.name)

    if note_with_same_name != None:
        raise NoteAlreadyExistsError(request_body.name)

    try:
        new_note = await create_note(session, request_body.name, request_body.text, response_validation["user_id"])
        return {
            "message": "Note created succesfully",
            "note": {
                "id": str(new_note.id),
                "name": new_note.name
            }
        }
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
    
    notes = await session.execute(select(Note).where(Note.user_id == response_validation["user_id"]))
    notes_list = []
    for note in notes.scalars().all():
        notes_list.append({
            "id": str(note.id),
            "name": note.name
        })

    await session.close()
    return {"notes": notes_list}
    

async def update_note_service(
        note_id: str,
        request_body: UpdateNoteRequest,
        session: AsyncSession,
        token: str
    ):

    data = {"token": token}
    response_validation = await validate_token(data)

    # проверка валидности токена
    if "email" not in response_validation.keys():
        return response_validation
    
    # проверка на наличие такой заметки для изменения
    existing_note = await get_note_by_id(session, note_id)
    if not existing_note:
        raise NoteNotFound(note_id)
    



