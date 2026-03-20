from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config.settings import settings

async_session_maker = async_sessionmaker(
    create_async_engine(url=settings.db.DB_URL),
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class SessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with async_session_maker() as session:
            try:
                data["session"] = session

                # res = await session.execute(select(User).where(User.tg_id == uid))
                # user: User = res.scalar_one_or_none()
                #
                # if user is None:
                #     user = User(tg_id=uid)
                #     session.add(user)
                #     await session.commit()
                #     await session.refresh(user, attribute_names=["packs"])
                #
                # data["user"] = user
                return await handler(event, data)
            finally:
                await session.close()
