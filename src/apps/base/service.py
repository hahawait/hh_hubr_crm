from src.apps.base.driver import Driver


class BaseService:
    def __init__(self, driver_path: str):
        self.driver = Driver(driver_path)
