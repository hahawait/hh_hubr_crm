from dataclasses import dataclass
from functools import lru_cache

from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(env_file="prod.env", extra="allow")


class FastAPISettings(BaseSettings):
    FASTAPI_HOST: str = "localhost"
    FASTAPI_PORT: int = 8000

    PROJECT_NAME: str = "FastAPI"
    VERSION: str = "1.0.0"


class DriverSettings(BaseSettings):
    DRIVER_PATH: str | None = 'driver/chromedriver.exe'


class HHSettings(BaseSettings):
    LOGIN: str
    PASSWORD: str


@dataclass
class Config:
    fastapi_settings: FastAPISettings
    driver_settings: DriverSettings
    hh_settings: HHSettings


@lru_cache
def get_config():
    return Config(
        fastapi_settings=FastAPISettings(),
        driver_settings=DriverSettings(),
        hh_settings=HHSettings(),
    )
