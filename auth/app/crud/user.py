import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def get_user_by_id(user_id: int, session: AsyncSession) -> [User, None]:
    """
    Фунция получения пользователя по id из таблицы user
    :param user_id: id пользователя
    :return: Объект пользователя
    """
    user = await session.execute(select(User).where(User.email == email))
    await session.close()
    return user.scalars().first()


async def get_user_by_email(email: str, session: AsyncSession) -> [User, None]:
    """
    Фунция получения пользователя по email из таблицы users
    :param email: email пользователя
    :return: Объект пользователя
    """
    user = await session.execute(select(User).where(User.email == email))
    await session.close()
    return user.scalars().first()