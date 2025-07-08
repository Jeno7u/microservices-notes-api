from pydantic import BaseModel
import uuid
from typing import List, Optional


class CreateNoteRequest(BaseModel):
    name: str
    text: str = None


class NoteResponse(BaseModel):
    id: uuid.UUID
    name: str
    text: Optional[str] = None
    user_id: uuid.UUID

    class Config:
        from_attributes = True


class NotesListResponse(BaseModel):
    notes: List[NoteResponse]
