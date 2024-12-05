from pydantic import BaseModel


class CreateUserForm(BaseModel):
    name: str
    telegram_id: int


class UpdateUserForm(BaseModel):
    name: str | None
    telegram_id: int | None


__all__ = ["CreateUserForm", "UpdateUserForm"]
