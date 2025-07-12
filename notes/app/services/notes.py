import jwt
import httpx

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.notes import CreateNoteRequest, UpdateNoteRequest
from app.schemas.response import ResponseBase
from app.core.security.utils import validate_token
from app.core.security.errors import NoteAlreadyExistsError, NoteNotFound, UnauthorizedNoteAccessError
from app.crud.note import get_note_by_user_and_name, get_note_by_id, create_note, update_note_by_user
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
    if request_body.name:
        note_with_same_name = await get_note_by_user_and_name(session, response_validation["user_id"], request_body.name)

        if note_with_same_name != None:
            raise NoteAlreadyExistsError(request_body.name)

    try:
        new_note = await create_note(session, response_validation["user_id"], request_body.name, request_body.text)
        await session.commit()
        return {
            "message": "Note created succesfully",
            "note": {
                "id": str(new_note.id),
                "name": new_note.name
            }
        }
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def get_notes_service(session: AsyncSession, token: str):
    try:
        response_validation = await validate_token({"token": token})

        notes = await session.execute(select(Note).where(Note.user_id == response_validation["user_id"]))
        notes_list = []
        for note in notes.scalars().all():
            notes_list.append({
                "id": str(note.id),
                "name": note.name
            })

        return {"notes": notes_list}
    finally:
        await session.close()
    

async def update_note_service(
        note_id: str,
        request_body: UpdateNoteRequest,
        session: AsyncSession,
        token: str
    ):
    try:
        data = {"token": token}
        response_validation = await validate_token(data)

        # проверка валидности токена
        if "email" not in response_validation.keys():
            return response_validation

        # проверка на наличие такой заметки для изменения
        existing_note = await get_note_by_id(session, note_id)
        if not existing_note:
            raise NoteNotFound(note_id)
        
        # проверка на принадлежность заметки пользователю
        if existing_note.user_id != response_validation["user_id"]:
            raise UnauthorizedNoteAccessError()
        
        # проверка на дубликат имени (если изменяется)
        if request_body.name and request_body.name != existing_note.name:
            note_with_same_name = await get_note_by_user_and_name(session, response_validation["user_id"], request_body.name)
            if note_with_same_name:
                raise NoteAlreadyExistsError(request_body.name)
        
        # нет изменений
        if request_body.name == None and request_body.text == None:
            return {
                "message": "No changes detected",
                "note": {
                    "id": note_id,
                    "name": existing_note.name
                }
            }
        
        name = existing_note.name if request_body.name == None else request_body.name

        await update_note_by_user(session, note_id, request_body.name, request_body.text)
        await session.commit()
        return {
            "message": "Note updated succesfully",
            "note": {
                "id": note_id,
                "name": name
            }
        }
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()

    

async def get_note_service(note_id: str, session: AsyncSession, token: str):
    try:
        data = {"token": token}
        response_validation = await validate_token(data)

        # проверка валидности токена
        if "email" not in response_validation.keys():
            return response_validation

        # проверка на наличие заметки с ID == note_id
        existing_note = await get_note_by_id(session, note_id)
        if not existing_note:
            raise NoteNotFound(note_id)
        
        # проверка на принадлежность заметки пользователю
        if existing_note.user_id != response_validation["user_id"]:
            raise UnauthorizedNoteAccessError()
        
        return {
            "message": "Note succesfully received",
            "note": {
                "id": note_id,
                "name": existing_note.name,
                "text": existing_note.text
            }
        }
    finally:
        await session.close()

