import uuid
from typing import List
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Note(Base):
    __tablename__ = "notes"
    __table_args__ = {"schema": "notes"}
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(40))
    text: Mapped[str] = mapped_column(Text, nullable=True)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, name={self.name!r}, user_id={self.user_id!r})"

