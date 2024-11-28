from contextlib import asynccontextmanager
from os import getenv
import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.start import start_router

_TOKEN = getenv("BOT_TOKEN")
_dispatcher: Dispatcher

@asynccontextmanager
async def bot_lifespan():
    global _dispatcher
    _dispatcher = Dispatcher()
    _dispatcher.include_routers(start_router)

    asyncio.get_event_loop().create_task(
        _dispatcher.start_polling(
            Bot(token=_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        )
    )
    try:
        yield
    finally:
        await _dispatcher.emit_shutdown()
        await _dispatcher.stop_polling()