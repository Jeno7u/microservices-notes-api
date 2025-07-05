from pydantic import BaseModel


class CreateNoteRequest(BaseModel):
    name: str = None
    text: str = None

