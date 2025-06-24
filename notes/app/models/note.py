import uuid
from typing import List
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models import User


class Note(Base):
    __tablename__ = "notes"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(Text)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    related_user: Mapped[User] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, text={self.text[:20]!r}, user_id={self.user_id!r})"

