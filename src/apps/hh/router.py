from fastapi import APIRouter, Depends
from fastapi.responses import Response

from apps.hh.service import HHService
from apps.hh.xlsx import create_excel_file
from apps.hh.dependencies import get_hh_service

hh_router = APIRouter(
    prefix="/hh",
    tags=["Парсер hh"],
)


@hh_router.get("/get_vacancy", description="Поинт для парсинга вакансий")
async def get_vacancy(
    url: str,
    start_page: int,
    end_page: int,
    hh_service: HHService = Depends(get_hh_service)
) -> Response:
    start_page -= 1
    vacancies = hh_service.get_vacancy(url, start_page, end_page)
    buffer = create_excel_file(vacancies)

    return Response(
        buffer.getvalue(), 
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        headers={"Content-Disposition": "attachment;filename=hh_vacancies.xlsx"}
    )

