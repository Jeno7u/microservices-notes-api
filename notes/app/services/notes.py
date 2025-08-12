from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from notes.app.schemas.notes import CreateNoteRequest, UpdateNoteRequest, NoteResponse, NoteTextResponse, NotesListResponse
from notes.app.core.security.utils import validate_token
from notes.app.core.security.errors import NoteAlreadyExistsError, NoteNotFound, UnauthorizedNoteAccessError, InternalServerError
from notes.app.crud.note import get_note_by_user_and_name, get_note_by_id, create_note, update_note_by_user, delete_note_by_id
from notes.app.models import Note


async def check_note_with_same_name(session: AsyncSession, note_name: str, user_id: str) -> None:
    """Проверка наличии заметки с таким же названием и принадлежащая пользователю"""
    if note_name:
        note_with_same_name = await get_note_by_user_and_name(session, user_id, note_name)

        if note_with_same_name is not None:
            raise NoteAlreadyExistsError(note_name)
        

async def check_note_existence(session: AsyncSession, note_id: str) -> Note:
    """Проверка наличии заметки с ID == note_id"""
    note = await get_note_by_id(session, note_id)
    if not note:
        raise NoteNotFound(note_id)
    return note
    

async def check_note_belongs_to_user(note_user_id: str, token_user_id: str) -> None:
    """Проверка принадлежности заметки пользователю"""
    if note_user_id != token_user_id:
        raise UnauthorizedNoteAccessError()
    

async def validate_note_access(session: AsyncSession, note_id: str, user_id: str) -> Note:
    """Проверка наличии заметки с ID == note_id и проверкой принадлежности данной заметки пользователю"""
    note = await check_note_existence(session, note_id)
    await check_note_belongs_to_user(str(note.user_id), user_id)
    return note
    

async def create_note_service(
        request_body: CreateNoteRequest, 
        session: AsyncSession, 
        token: str
    ) -> NoteResponse:
    response_validation = await validate_token(token)

    await check_note_with_same_name(session, request_body.name, response_validation["user_id"])

    try:
        new_note = await create_note(session, response_validation["user_id"], request_body.name)
        await session.flush()
        
        note_id = str(new_note.id)
        note_name = new_note.name

        await session.commit()
        
        return {
                "id": note_id,
                "name": note_name
        }
    
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def get_notes_service(session: AsyncSession, token: str) -> NotesListResponse:
    try:
        response_validation = await validate_token(token)

        notes = await session.execute(
            select(Note).where(
                Note.user_id == response_validation["user_id"]
                )
            )
        notes_list = []
        for note in notes.scalars().all():
            notes_list.append({
                "id": str(note.id),
                "name": note.name
            })

        return {"notes": notes_list}
    except Exception as e:
        raise e
    finally:
        await session.close()
    

async def update_note_service(
        note_id: str,
        request_body: UpdateNoteRequest,
        session: AsyncSession,
        token: str
    ) -> NoteResponse:
    try:
        response_validation = await validate_token(token)

        note = await validate_note_access(session, note_id, response_validation["user_id"])
        
        # проверка на дубликат имени (если изменяется)
        if request_body.name and request_body.name != note.name:
            await check_note_with_same_name(session, request_body.name, response_validation["user_id"])
        
        # нет изменений
        if request_body.name is None and request_body.text is None:
            return {
                "id": note_id,
                "name": note.name
            }
        
        name = note.name if request_body.name is None else request_body.name

        await update_note_by_user(session, note_id, request_body.name, request_body.text)
        await session.commit()
        return {
            "id": note_id,
            "name": name
        }
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()

    

async def get_note_service(note_id: str, session: AsyncSession, token: str) -> NoteTextResponse:
    try:
        response_validation = await validate_token(token)

        note = await validate_note_access(session, note_id, response_validation["user_id"])
        
        return {
            "id": note_id,
            "name": note.name,
            "text": note.text
        }
    except Exception as e:
        raise e
    finally:
        await session.close()



async def delete_note_service(note_id: str, session: AsyncSession, token: str):
    try:
        response_validation = await validate_token(token)

        note = await validate_note_access(session, note_id, response_validation["user_id"])
        
        await delete_note_by_id(note_id, session)
        await session.commit()
    
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()