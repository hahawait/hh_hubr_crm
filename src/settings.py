from typing import Literal
from functools import lru_cache
from dataclasses import dataclass

from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings as PydanticSettings


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(env_file="prod.env", extra="allow")


class FastAPISettings(BaseSettings):
    LOGGING_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"] = "INFO"
    FASTAPI_HOST: str = "localhost"
    FASTAPI_PORT: int = 8000

    PROJECT_NAME: str = "FastAPI"
    VERSION: str = "1.0.0"


class DriverSettings(BaseSettings):
    DRIVER_PATH: str | None = 'driver/chromedriver.exe'


class HHSettings(BaseSettings):
    HH_LOGIN: str
    HH_PASSWORD: str


class HubrSettings(BaseSettings):
    HUBR_EMAIL: str
    HUBR_PASSWORD: str


@dataclass
class Config:
    fastapi_settings: FastAPISettings
    driver_settings: DriverSettings
    hh_settings: HHSettings
    hubr_settings: HubrSettings


@lru_cache
def get_config():
    return Config(
        fastapi_settings=FastAPISettings(),
        driver_settings=DriverSettings(),
        hh_settings=HHSettings(),
        hubr_settings=HubrSettings(),
    )
