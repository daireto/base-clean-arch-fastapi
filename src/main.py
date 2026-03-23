from app.app import create_production_app
from app.config import settings
from app.logger import global_app_logger, setup_log_rotation

if settings.use_log_rotation:
    setup_log_rotation(
        loggers=[global_app_logger],
        filepath=settings.logs_path,
    )


app = create_production_app()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.port,
        log_config=None,
        reload=settings.is_dev,
    )
