from core.app import create_default_app
from core.config import settings

app = create_default_app()

# TODO: Add Users and Auth
# TODO: Relate Users to Resources
# TODO: Add MCP server (use main.py as entry point for both FastAPI and MCP server)
# TODO: Add LLM integration

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.server.port,
        log_config=None,
        reload=settings.server.is_dev,
        forwarded_allow_ips='*' if settings.server.behind_proxy else None,
    )
