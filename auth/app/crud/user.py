from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.app.models import User


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    """Returns user by email"""
    user = await session.execute(select(User).where(User.email == email))
    return user.scalars().first()


async def get_user_by_login(login: str, session: AsyncSession) -> User:
    """Returns user by login"""
    user = await session.execute(select(User).where(User.login == login))
    return user.scalars().first()
