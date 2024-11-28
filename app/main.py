from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.security import auth_router
from app.db import db_lifespan
from app.bot import bot_lifespan

@asynccontextmanager
async def app_lifespan(app: FastAPI):  # noqa
    async with db_lifespan():
        async with bot_lifespan():
            yield


app = FastAPI(lifespan=app_lifespan)

app.include_router(auth_router)
app.include_router(api_router)
