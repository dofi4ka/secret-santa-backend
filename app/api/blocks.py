from fastapi import Depends, HTTPException, status

from app.api.router import api_router
from app.core.security import get_current_admin
from app.db import get_db_querier, AsyncQuerier
from app.db.models import Admin, UserBlock
from app.db.query import ListUserBlocksRow


@api_router.get("/users/{blocker_id}/blocks")
async def list_user_blocks(
        blocker_id: int,
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(get_db_querier)
) -> list[ListUserBlocksRow]:
    if not querier.check_user_exists(id=blocker_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified id is not found"
        )
    blocks: list[ListUserBlocksRow] = []
    async for block in querier.list_user_blocks(blocker_id=blocker_id):
        blocks.append(block)
    return blocks


@api_router.post("/users/{blocker_id}/blocks/{blocked_id}")
async def block_user(
        blocker_id: int,
        blocked_id: int,
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(get_db_querier)
) -> UserBlock:
    if not querier.check_user_exists(id=blocker_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified id is not found"
        )
    return await querier.block_user(blocked_id=blocked_id, blocker_id=blocker_id)  # todo error handling


@api_router.delete("/users/{blocker_id}/blocks/{blocked_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unblock_user(
        blocker_id: int,
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(get_db_querier)
):
    if not await querier.check_user_exists(id=blocker_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified id is not found"
        )
    await querier.delete_user(id=blocker_id)
