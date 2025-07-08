from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.notes import create_note_service, get_notes_service
from app.schemas.notes import CreateNoteRequest, NotesListResponse
from app.core.security.utils import get_current_token


router = APIRouter()


@router.post("/create/")
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


@router.get("/")
async def get_notes(
    session: AsyncSession = Depends(get_db), 
    token: str = Depends(get_current_token)
    ):
    """
    Получения списка заметок пользователя
    """
    response = await get_notes_service(session, token)

    return response


@router.update("/update")
async def update_note(
    session: AsyncSession = Depends(get_db),
    token: str = Depends(get_current_token)
)
# changing note
# deleting note
