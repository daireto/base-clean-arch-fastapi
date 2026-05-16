from app import create_default_app
from config import settings

app = create_default_app()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.server.port,
        log_config=None,
        reload=settings.is_dev,
    )
