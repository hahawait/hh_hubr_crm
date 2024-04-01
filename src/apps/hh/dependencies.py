from apps.base.dependencies import get_dependencies

from apps.hh.service import HHService


def get_hh_service() -> HHService:
    config, driver = get_dependencies()
    return HHService(
        config, driver
    )
