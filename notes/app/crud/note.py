from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note


async def get_note_by_user_and_name(session: AsyncSession, user_id: str, name: str) -> Note:
    """Получение заметки через ID пользователя и названия заметки"""
    note_by_name = await session.execute(
        select(Note).where(
            Note.user_id == user_id, 
            Note.name == name
        )
    )
    return note_by_name.scalars().first()


async def get_note_by_id(session: AsyncSession, note_id: str) -> Note:
    note_by_id = await session.execute(
        select(Note).where(
            Note.id == note_id
        )
    )
    return note_by_id.scalars().first()


async def create_note(
        session: AsyncSession, 
        user_id: str,
        name: Optional[str] = None, 
        text: Optional[str] = None, 
        base_name: str = "New Note"
) -> Note:
    """Создание заметки с возможностью оставить стандартное название"""

    # создание стандартного названия если не задано иначе
    if not name:
        pattern = f"{base_name} %"
        existing_notes = await session.execute(
            select(Note.name).where(
                Note.user_id == user_id, 
                Note.name.like(pattern)
            )
        )
        used_numbers = []
        for name in existing_notes.sclalars().all():
            if name.startswith(f"{base_name} "):
                suffix = name[len(f"{base_name} "):]
                if suffix.isdigit():
                    used_numbers.append(int(suffix))
        
        counter = 1
        while counter in used_numbers:
            counter += 1

        name = f"{base_name} {counter}"

    new_note = Note(
        name=name,
        text=text,
        user_id=user_id
    )

    session.add(new_note)
    await session.commit()
    await session.close()
    return new_note