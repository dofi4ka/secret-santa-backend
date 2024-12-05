from fastapi import Depends, HTTPException, status, Body

from app.api.router import api_router
from app.core.security import get_current_admin
from app.db import (
    db_querier_gen, AsyncQuerier,
    ListUsersRow, CreateUserRow,
    User, Admin
)
from app.schemas import CreateUserForm, UpdateUserForm


@api_router.get("/users")
async def list_users(
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(db_querier_gen)
) -> list[ListUsersRow]:
    users: list[ListUsersRow] = []
    async for user in querier.list_users():
        users.append(user)
    return users


@api_router.post("/users")
async def create_user(
        _: Admin = Depends(get_current_admin),
        data: CreateUserForm = Body(...),
        querier: AsyncQuerier = Depends(db_querier_gen)
) -> CreateUserRow | None:
    return await querier.create_user(name=data.name, telegram_id=data.telegram_id)  # todo error handling


@api_router.put("/users/{user_id}")
async def update_user(
        user_id: int,
        _: Admin = Depends(get_current_admin),
        data: UpdateUserForm = Body(...),
        querier: AsyncQuerier = Depends(db_querier_gen)
) -> User | None:
    user = await querier.check_user_exists(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified id is not found"
        )
    return await querier.update_user(id=user_id, name=data.name, telegram_id=data.telegram_id)


@api_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        _: Admin = Depends(get_current_admin),
        querier: AsyncQuerier = Depends(db_querier_gen)
):
    user = await querier.check_user_exists(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with specified id is not found"
        )
    await querier.delete_user(id=user_id)
