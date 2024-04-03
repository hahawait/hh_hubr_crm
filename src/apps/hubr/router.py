from fastapi import APIRouter, Depends

from apps.hubr.service import HubrService
from apps.hubr.dependencies import get_hubr_service
from apps.hubr.models import CompanyModel, VacancyModel, CompanyContactMembersModel


hubr_router = APIRouter(
    prefix="/hubr",
    tags=["Парсер hubr"],
)


@hubr_router.get("/get_companies_url", description="Поинт для парсинга URL компаний")
async def get_companies_url(
    url: str, 
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[str]:
    return hubr_service.get_companies_url(url)


@hubr_router.post("/get_company_contacts", description="Поинт для парсинга контактов компаний")
async def get_company_contacts(
    urls: list[str],
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[CompanyModel]:
    companies_contacts = []

    for url in urls:
        hubr_service.driver.driver.get(url)
        companies_contacts.append(hubr_service.get_company_contacts())
    hubr_service.driver.driver.close()
    return companies_contacts


@hubr_router.post("/get_company_contacts_members", description="Поинт для парсинга контактных лиц компаний (Требуется авторизация)")
async def get_company_contacts_members(
    urls: list[str],
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[CompanyContactMembersModel]:
    companies_contacts_members = []

    hubr_service._auth()
    hubr_service.driver.driver.get(urls[0])
    input("Нажали войти...\n")

    for url in urls:
        hubr_service.driver.driver.get(url)
        company_contact_members = hubr_service.get_company_contact_members()
        if not company_contact_members:
            hubr_service.driver.driver.close()
            return companies_contacts_members
        companies_contacts_members.append(company_contact_members)
    hubr_service.driver.driver.close()
    return companies_contacts_members


@hubr_router.get("/get_vacancy", description="Поинт для парсинга вакансий")
async def get_vacancy(
    url: str,
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[VacancyModel]:
    return hubr_service.get_vacancy_list(url)