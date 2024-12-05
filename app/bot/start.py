from app.db import db_querier_context

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.bot.messages import START_USER_FOUND, START_USER_NOT_FOUND

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def command_start_handler(message: Message):
    async with db_querier_context() as querier:
        user = await querier.get_user_by_telegram_id(telegram_id=message.from_user.id)
        if user is None:
            await message.answer(START_USER_NOT_FOUND.render())
        else:
            await message.answer(START_USER_FOUND.render(name=user.name))

        await querier.add_telegram_user(id=message.from_user.id)
