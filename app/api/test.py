from fastapi import Depends

from app.api.router import api_router
from app.core.security import get_current_admin
from app.db import db_querier_gen, AsyncQuerier
from app.db.models import Admin


@api_router.post("/add-telegram-user/{telegram_id}")
async def activate_telegram(
        telegram_id: int,
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(db_querier_gen)
):
    await querier.add_telegram_user(id=telegram_id)
