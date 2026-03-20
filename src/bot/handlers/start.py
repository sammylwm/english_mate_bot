from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def call(ms: Message):
    await ms.answer("test")
