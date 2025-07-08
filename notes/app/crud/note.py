from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note


async def get_note_by_name(session: AsyncSession, user_id: str, name: str) -> Note:
    """Getting user note by name"""
    note_by_name = await session.execute(select(Note).where(Note.user_id == user_id, Note.name == name))
    return note_by_name.scalars().first()