from apps.base.dependencies import get_dependencies

from apps.hubr.service import HubrService


def get_hubr_service() -> HubrService:
    config, driver = get_dependencies()

    return HubrService(config, driver)
