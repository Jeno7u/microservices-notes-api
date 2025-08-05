import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        {"schema": "auth"},
    )
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(25), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(70))
    second_name: Mapped[str] = mapped_column(String(40), nullable=True)
    email: Mapped[str] = mapped_column(String(70), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name=\"{self.surname} {self.name} {self.second_name}\", email={self.email!r}, is_admin={self.is_admin!r})"

