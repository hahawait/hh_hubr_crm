from fastapi import FastAPI

from apps.hh.router import hh_router
from settings import Config


def get_app(config: Config):
    fastapi_params = dict(
        title=config.fastapi_settings.PROJECT_NAME,
        version=config.fastapi_settings.VERSION,
    )

    app = FastAPI(**fastapi_params, debug=False)

    app.include_router(hh_router)

    return app
