import httpx
from fastapi import APIRouter, Request, status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.notes import NoteResponse, CreateNoteRequest, NotesListResponse, UpdateNoteRequest, NoteTextResponse
from app.schemas.response import ErrorResponse


security = HTTPBearer()
router = APIRouter()

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def make_request(
        self,
        method: str,
        endpoint: str,
        json_data=None,
        headers=None,
        expected_status=200
    ):
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                json=json_data,
                headers=headers
            )

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid authorization token")
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="No rights to access this note")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Note not found")
            elif response.status_code == 409:
                raise HTTPException(status_code=409, detail="Note with same name already exists")
            elif response.status_code == 422:
                raise HTTPException(status_code=422, detail="Validation error")
            elif response.status_code != expected_status:
                raise HTTPException(status_code=500, detail="Service unavailable")

            return response.json()
            

notes_client = ServiceClient("http://notes:8000")



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
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """Создание заметки пользователя"""
    headers = {"Authorization": f"Bearer {credentials.credentials}"}
    response = await notes_client.make_request(
        method="post",
        endpoint="/notes/create/",
        json_data=request_body.model_dump(),
        headers=headers,
        expected_status=201
    )

    return response


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=NotesListResponse,
            responses={
                401: {"model": ErrorResponse, "description": "Invalid authorization token"},
            })
async def get_notes(
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """Получения списка заметок пользователя"""
    headers = {"Authorization": f"Bearer {credentials.credentials}"}
    response = await notes_client.make_request(
        method="get",
        endpoint="/notes/",
        headers=headers,
        expected_status=200
    )

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
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """Обновление данных заметки"""
    headers = {"Authorization": f"Bearer {credentials.credentials}"}
    response = await notes_client.make_request(
        method="put",
        endpoint=f"/notes/{note_id}/",
        json_data=request_body.model_dump(),
        headers=headers,
        expected_status=200
    )

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
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """Получение данных заметки по ID заметки"""
    headers = {"Authorization": f"Bearer {credentials.credentials}"}
    response = await notes_client.make_request(
        method="get",
        endpoint=f"/notes/{note_id}/",
        headers=headers,
        expected_status=200
    )

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
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    """Удаление заметки по ID"""
    headers = {"Authorization": f"Bearer {credentials.credentials}"}
    await notes_client.make_request(
        method="delete",
        endpoint=f"/notes/{note_id}/",
        headers=headers,
        expected_status=204
    )