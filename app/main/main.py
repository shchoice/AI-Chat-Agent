import uvicorn
from fastapi import FastAPI

from common.loader import load_yaml
# from bootstrap.controller.vector_store_controller import vector_store_router

from bootstrap.router.router_registry import RouterRegistry
from config import constants
from config.settings import get_settings


def create_app() -> FastAPI:
    app = FastAPI()
    settings = get_settings()

    router_registry = RouterRegistry()
    # router_registry.register(vector_store_router)

    for router in router_registry.get_registered_routers():
        app.include_router(router, prefix=settings.API_V1_PREFIX)
    
    return app

app = create_app()

if __name__ == '__main__':
    uvicorn_config = load_yaml(constants.CONFIG_UVICORN_YAML_FILE_NAME)
    uvicorn.run(
        app=app,
        host=uvicorn_config['host'],
        port=uvicorn_config['port'],
        workers=uvicorn_config['workers'],
        log_level=uvicorn_config['log_level'],
        timeout_keep_alive=uvicorn_config['timeout_keep_alive'],
        reload=False
    )