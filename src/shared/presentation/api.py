from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from core.health import server_health
from shared.presentation.dtos import ServerHealthResponse

router = APIRouter(
    prefix='/health',
    tags=['health'],
    route_class=DishkaRoute,
)


@router.get('/')
def read_health() -> ServerHealthResponse:
    return ServerHealthResponse(
        message='ok'
        if server_health.is_healthy
        else server_health.get_unhealthy_reason(),
        healthy=server_health.is_healthy,
    )
