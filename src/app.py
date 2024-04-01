from fastapi import FastAPI

from settings import Config
from logger.logger import init_logger

from apps.hh.router import hh_router


def get_app(config: Config):
    init_logger(config.fastapi_settings.LOGGING_LEVEL)

    fastapi_params = dict(
        title=config.fastapi_settings.PROJECT_NAME,
        version=config.fastapi_settings.VERSION,
    )

    app = FastAPI(**fastapi_params)

    app.include_router(hh_router)

    return app
