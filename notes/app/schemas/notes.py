import uuid
from typing import List, Optional

from pydantic import BaseModel


class CreateNoteRequest(BaseModel):
    name: str = None

    class Config:
        schema_extra = {
            "exmaple": {
                "name": "My Todo List",
            }
        }


class UpdateNoteRequest(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Updated Note Name",
                "text": "Updated content"
            }
        }


class NoteResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        schema_extra = {
            "example" : {
                "id": "d3c3a3e7-9613-452a-9d9f-31d2cfb0db96",
                "name": "My Todo List"
            }
        }


class NotesListResponse(BaseModel):
    notes: List[NoteResponse]
