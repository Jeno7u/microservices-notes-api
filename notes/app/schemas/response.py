from typing import Optional

from pydantic import BaseModel


class ResponseBase(BaseModel):
    code: int
    description: str = None



class ErrorResponse(BaseModel):
    detail: str
    error: Optional[str] = None