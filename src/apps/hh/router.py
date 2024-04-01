from fastapi import APIRouter

from apps.hh.service import HHService
from settings import get_config
from apps.base.driver import Driver

hh_router = APIRouter(
    prefix="/hh",
    tags=["Парсер hh"],
)


@hh_router.post("/auth")
async def hh_auth(url: str):
    config = get_config()
    driver = Driver(config.driver_settings)
    hh_service = HHService(config, driver)
    hh_service.hh_auth(url)
    return {"message": "Authentication completed successfully"}
