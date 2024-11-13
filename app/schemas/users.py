from pydantic import BaseModel

class CreateUserFrom(BaseModel):
    name: str
    telegram_id: int

class UpdateUserFrom(BaseModel):
    name: str | None
    telegram_id: int | None


