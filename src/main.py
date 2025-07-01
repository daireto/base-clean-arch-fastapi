from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlactive import DBConnection

from resources.api import router as resources_router
from resources.infrastructure.models import DBModel as ResourcesDBModel
from shared.api import router as shared_router
from shared.config import SharedSettings

conn = DBConnection(SharedSettings.DATABASE_URL, echo=False)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await conn.init_db(ResourcesDBModel)
    yield


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(shared_router)
app.include_router(resources_router)
