from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import sess


async def create_session() -> AsyncGenerator[AsyncSession, None]:
    async with sess() as session:
        yield session
