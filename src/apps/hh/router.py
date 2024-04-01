from fastapi import APIRouter, Depends

from apps.hh.service import HHService
from apps.hh.schemas import HHResponce
from apps.hh.dependencies import get_hh_service

hh_router = APIRouter(
    prefix="/hh",
    tags=["Парсер hh"],
)


@hh_router.get("/get_vacancy")
async def get_vacancy(
    url: str,
    start_page: int,
    end_page: int,
    hh_service: HHService = Depends(get_hh_service)
) -> HHResponce:
    return hh_service.get_vacancy(url, start_page, end_page)
