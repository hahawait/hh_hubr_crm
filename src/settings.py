from dataclasses import dataclass
from functools import lru_cache

from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(env_file="prod.env", extra="allow")


class DriverSettings(BaseSettings):
    DRIVER_PATH: str | None = 'driver/chromedriver.exe'


class HHSettings(BaseSettings):
    LOGIN: str
    PASSWORD: str


@dataclass
class Config:
    driver_settings: DriverSettings
    hh_setting: HHSettings


@lru_cache
def get_config():
    return Config(
        driver_settings=DriverSettings(),
        hh_setting=HHSettings(),
    )
