from app.bot import bot_instance

from app.bot.messages import BROADCAST


async def send_broadcast_message(chat_id, recepient: str):
    await bot_instance.send_message(chat_id, BROADCAST.render(recepient=recepient))
