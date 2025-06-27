from pydantic import BaseModel


class ResponseBase(BaseModel):
    code: int
    description: str = None

