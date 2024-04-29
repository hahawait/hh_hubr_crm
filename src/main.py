import uvicorn

from app import get_app
from settings import get_config

config = get_config()
app = get_app(config=config)


if __name__ == "__main__":
    host = config.fastapi_settings.FASTAPI_HOST
    port = config.fastapi_settings.FASTAPI_PORT
    uvicorn.run(app, host=host, port=port)
    # uvicorn.run('main:app', host=host, port=port, reload=True)
