from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    error: Optional[str] = None