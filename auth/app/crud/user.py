from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    """
    Фунция получения пользователя по email из таблицы users
    :param email: email пользователя
    :return: Объект пользователя
    """
    user = await session.execute(select(User).where(User.email == email))
    return user.scalars().first()