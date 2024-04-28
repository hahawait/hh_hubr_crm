import json

from fastapi import APIRouter, Depends, Response, File, UploadFile

from apps.hubr import xlsx
from apps.hubr.service import HubrService
from apps.hubr.zip import generate_zip_and_response
from apps.hubr.dependencies import get_hubr_service
from apps.hubr.models import CompanyContactMembersUrlsModel, CompanyContactMembersModel


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
) -> Response:
    companies_contacts = []

    for url in urls:
        hubr_service.driver.driver.get(url)
        companies_contacts.append(hubr_service.get_company_contacts())
    hubr_service.driver.driver.close()

    buffer = xlsx.create_company_contacts_excel(companies_contacts)

    return Response(
        buffer.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment;filename=company_contacts.xlsx"}
    )


@hubr_router.post("/get_company_contacts_members", description="Поинт для парсинга контактных лиц компаний (Требуется авторизация)")
async def get_company_contacts_members(
    contact_members_json: UploadFile = File(..., description="JSON-файл с данными о контактных лицах компаний"),
    auth_data_file: UploadFile = File(..., description="Файл в формате .txt с данными для аутентификации"),
    hubr_service: HubrService = Depends(get_hubr_service)
):
    # Чтение содержимого JSON-файла
    contact_members_data = await contact_members_json.read()

    companies_contact_members_urls = [CompanyContactMembersUrlsModel(**item) for item in json.loads(contact_members_data)]

    # Прочитать данные из файла .txt
    auth_data_content = await auth_data_file.read()
    # Разбить содержимое файла по строкам и создать список кортежей (email, password)
    auth_data = [line.strip().split(":") for line in auth_data_content.decode().split("\n") if line.strip()]

    limit = False
    total_urls = 0
    target_account_num = 0
    companies_contacts_members = []

    for i, company_contact_members_url in enumerate(companies_contact_members_urls):
        company_contact_members = CompanyContactMembersModel(company_name=company_contact_members_url.company_name)
        for j, url in enumerate(company_contact_members_url.contact_members_urls):
            if total_urls >= len(auth_data) * 10:
                remaining_contact_members = companies_contact_members_urls[i+1:] if i + 1 <= len(companies_contact_members_urls) else []
                remaining_contact_members.append(
                    CompanyContactMembersUrlsModel(
                        company_name=company_contact_members_url.company_name,
                        contact_members_urls=company_contact_members_url.contact_members_urls[j:] if j <= len(company_contact_members_url.contact_members_urls) else []
                    )
                )

                limit = True
                break

            if total_urls % 10 == 0:
                hubr_service.driver.restart()
                hubr_service._auth(auth_data[target_account_num][0], auth_data[target_account_num][1])
                target_account_num += 1

            contact = hubr_service.get_company_contact_member(url)
            total_urls += 1

            company_contact_members.contact_members.append(contact)

        companies_contacts_members.append(company_contact_members)

        if limit is True:
            break

    hubr_service.driver.driver.close()

    buffer = xlsx.create_company_contacts_members_excel(companies_contacts_members)

    if limit is True:
        return generate_zip_and_response(buffer, remaining_contact_members)
    else:
        return Response(
            buffer.getvalue(),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment;filename=Companies_contacts_members.xlsx"}
        )


@hubr_router.post("/get_company_contacts_members_urls", description="Поинт для парсинга ссылок на контактные лица компаний")
async def get_company_contacts_members_urls(
    urls: list[str],
    hubr_service: HubrService = Depends(get_hubr_service)
) -> list[CompanyContactMembersUrlsModel]:
    companies_contacts_members_urls = []

    for url in urls:
        hubr_service.driver.driver.get(url)
        company_name=hubr_service.driver.find_by_class_name('company_name').text
        urls = hubr_service.get_company_contact_members_urls()
        companies_contacts_members_urls.append(
            CompanyContactMembersUrlsModel(
                company_name=company_name,
                contact_members_urls=urls
            )
        )
    hubr_service.driver.driver.close()
    return companies_contacts_members_urls


@hubr_router.get("/get_vacancy", description="Поинт для парсинга вакансий")
async def get_vacancy(
    url: str,
    hubr_service: HubrService = Depends(get_hubr_service)
) -> Response:
    vacancy_list = hubr_service.get_vacancy_list(url)

    buffer = xlsx.create_vacancy_excel(vacancy_list)

    return Response(
        buffer.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment;filename=Vacancies.xlsx"}
    )
