from settings import get_config
from apps.base.driver import Driver


def get_dependencies():
    config = get_config()
    driver = Driver(config.driver_settings)
    return config, driver
