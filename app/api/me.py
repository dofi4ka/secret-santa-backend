from fastapi import Depends

from app.api.router import api_router
from app.core.security import get_current_admin
from app.db import AsyncQuerier, db_querier_gen
from app.db.models import Admin


@api_router.get("/me")
async def admin_info(
        admin: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(db_querier_gen)
) -> Admin:
    return await querier.get_admin(username=admin.username)