from fastapi import APIRouter, Depends

from apps.hubr.service import HubrService
from apps.hubr.models import CompanyModel
from apps.hubr.dependencies import get_hubr_service


hubr_router = APIRouter(
    prefix="/hubr",
    tags=["Парсер hubr"],
)


@hubr_router.get("/get_companies_url")
async def get_companies_url(
    url: str, 
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[str]:
    return hubr_service.get_companies_url(url)


@hubr_router.post("/get_company_contacts")
async def get_company_contacts(
    urls: list[str],
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[CompanyModel]:
    return hubr_service.get_companies_contacts(urls)
