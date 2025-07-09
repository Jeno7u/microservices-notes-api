from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.notes import create_note_service, get_notes_service, update_note_service
from app.schemas.notes import CreateNoteRequest, NoteResponse, NotesListResponse, UpdateNoteRequest
from app.schemas.response import ErrorResponse
from app.core.security.utils import get_current_token


router = APIRouter()


@router.post("/create/",
             status_code=status.HTTP_201_CREATED,
             response_model=NoteResponse,
             responses={
                 401: {"model": ErrorResponse, "description": "Invalid autorization token"},
                 409: {"model": ErrorResponse, "description": "Note with same name already exists"},
                 422: {"model": ErrorResponse, "description": "Validation error"}
            })
async def create_note(
    request_body: CreateNoteRequest, 
    session: AsyncSession = Depends(get_db),
    token: str = Depends(get_current_token)
    ):
    """
    Создание заметки пользователя
    """
    response = await create_note_service(request_body, session, token)

    return response


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=NotesListResponse,
            responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
            })
async def get_notes(
    session: AsyncSession = Depends(get_db), 
    token: str = Depends(get_current_token)
    ):
    """
    Получения списка заметок пользователя
    """
    response = await get_notes_service(session, token)

    return response


@router.put("/{note_id}",
            status_code=status.HTTP_200_OK,
            response_model=NoteResponse,
            responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
                404: {"model": ErrorResponse, "description": "Note not found"},
                409: {"model": ErrorResponse, "description": "Note with same name already exists"}
            })
async def update_note(
    note_id: str,
    request_body: UpdateNoteRequest,
    session: AsyncSession = Depends(get_db),
    token: str = Depends(get_current_token)
    ):
    """
    Обновление данных заметки
    """
    response = await update_note_service(note_id, request_body, session, token)

    return response

# deleting note
