from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.notes import create_note_service, get_notes_service, update_note_service, get_note_service, delete_note_service
from app.schemas.notes import CreateNoteRequest, NoteResponse, NotesListResponse, UpdateNoteRequest, NoteTextResponse
from app.schemas.response import ErrorResponse


security = HTTPBearer()
router = APIRouter()


@router.post("/create/",
             status_code=status.HTTP_201_CREATED,
             response_model=NoteResponse,
             responses={
                 401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                 409: {"model": ErrorResponse, "description": "Note with same name already exists"},
                 422: {"model": ErrorResponse, "description": "Validation error"}
            })
async def create_note(
    request_body: CreateNoteRequest, 
    session: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """
    Создание заметки пользователя
    """
    response = await create_note_service(request_body, session, credentials.credentials)

    return response


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=NotesListResponse,
            responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
            })
async def get_notes(
    session: AsyncSession = Depends(get_db), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """
    Получения списка заметок пользователя
    """
    response = await get_notes_service(session, credentials.credentials)

    return response


@router.put("/{note_id}/",
            status_code=status.HTTP_200_OK,
            response_model=NoteResponse,
            responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                403: {"model": ErrorResponse, "description": "No rights to access this note"},
                404: {"model": ErrorResponse, "description": "Note not found"},
                409: {"model": ErrorResponse, "description": "Note with same name already exists"},
                422: {"model": ErrorResponse, "description": "Validation error"}
            })
async def update_note(
    note_id: str,
    request_body: UpdateNoteRequest,
    session: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """
    Обновление данных заметки
    """
    response = await update_note_service(note_id, request_body, session, credentials.credentials)

    return response


@router.get("/{note_id}/",
            status_code=status.HTTP_200_OK,
            response_model=NoteTextResponse,
            responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                403: {"model": ErrorResponse, "description": "No rights to acess this note"},
                404: {"model": ErrorResponse, "description": "Note not found"},
            })
async def get_note(
    note_id: str,
    session: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """
    Получение данных заметки по ID заметки
    """
    response = await get_note_service(note_id, session, credentials.credentials)

    return response


@router.delete("/{note_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                403: {"model": ErrorResponse, "description": "No rights to acess this note"},
                404: {"model": ErrorResponse, "description": "Note not found"},
                })
async def delete_note(
    note_id: str,
    session: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """
    Удаление заметки по ID
    """
    await delete_note_service(note_id, session, credentials.credentials)
