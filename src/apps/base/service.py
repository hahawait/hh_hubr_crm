from apps.base.driver import Driver
from settings import Config


class BaseService:
    def __init__(self, config: Config, driver: Driver):
        self.config = config
        self.driver = driver
