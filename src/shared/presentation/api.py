from fastapi import APIRouter

from health import ServerHealthResponse, server_health

router = APIRouter()


@router.get('/health')
def read_health() -> ServerHealthResponse:
    """Health check endpoint.

    Returns
    -------
    ServerHealthResponse
        Health check response.

    Examples
    --------
    Healthy response:
    >>> import httpx
    >>> httpx.get('http://localhost:8000/health').json()
    {'message': 'ok', 'healthy': True}

    Unhealthy response:
    >>> import httpx
    >>> httpx.get('http://localhost:8000/health').json()
    {'message': 'Database is not available', 'healthy': False}

    """
    return server_health.to_response()
