from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from core.health import ServerHealthResponse, server_health

router = APIRouter(
    prefix='/health',
    tags=['health'],
    route_class=DishkaRoute,
)


@router.get('/')
def read_health() -> ServerHealthResponse:
    return server_health.to_response()
