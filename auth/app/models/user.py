import uuid
from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(25))
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(70))
    second_name: Mapped[str] = mapped_column(String(40), nullable=True)
    email: Mapped[str] = mapped_column(String(70))
    password: Mapped[str] = mapped_column(String(97))
    is_admin: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name=\"{self.surname} {self.name} {self.second_name}\", email={self.email!r}, is_admin={self.is_teacher!r})"

