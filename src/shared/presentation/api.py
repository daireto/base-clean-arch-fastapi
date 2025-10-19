from fastapi import APIRouter

from src.core.health import server_health

router = APIRouter()


@router.get('/health')
@router.get('/ping')
def read_health() -> dict[str, str]:
    return server_health.to_response()
