from fastapi import Depends

from app.api.router import api_router
from app.core.security import get_current_admin
from app.db import (
    db_querier_gen, AsyncQuerier,
    ListUsersRow,
    Admin
)
from app.utils import distribution_with_banlist

from app.bot.broadcast import send_broadcast_message


@api_router.post("/distribute")
async def distribute_users(
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(db_querier_gen)
):
    users: dict[int, ListUsersRow] = {}
    distribution_participiants: dict[int, set[int]] = {}
    async for user in querier.list_users():
        distribution_participiants[user.id] = set(user.users_blocked)
        distribution_participiants[user.id].add(user.id)
        users[user.id] = user

    distributed = distribution_with_banlist(distribution_participiants)

    for user in users.values():
        recepient = users[distributed[user.id]]
        print(f"{user.name} -> {recepient.name}")
        if user.telegram_activated:
            await send_broadcast_message(user.telegram_id, recepient.name)
