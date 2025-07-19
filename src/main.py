from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlactive import DBConnection

from resources.api import router as resources_router
from resources.infrastructure.models.sqlite import SQLiteDBModel as ResourcesDBModel
from shared import settings
from shared.api import router as shared_router

conn = DBConnection(settings.DATABASE_URL, echo=False)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    base_models = [
        ResourcesDBModel,
    ]
    for model in base_models:
        await conn.init_db(model)
    yield


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(shared_router)
app.include_router(resources_router)
