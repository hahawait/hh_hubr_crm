from io import BytesIO
from openpyxl import Workbook

from apps.hh.models import VacancyModel


def create_excel_file(vacancies: list[VacancyModel]) -> BytesIO:
    # Создаем новую книгу Excel
    wb = Workbook()
    ws = wb.active

    # Настройка заголовков колонок
    headers = [
        "Название вакансии",
        "Название компании",
        "Контактное лицо",
        "Телефон 1",
        "Телефон 2",
        "Email",
        "Зарплата",
        "Описание",
        "Ссылка на вакансию"
    ]

    ws.append(headers)

    # Заполняем данные в книгу
    for vacancy in vacancies:
        ws.append([
            vacancy.vacancy_name,
            vacancy.company_name,
            vacancy.contact_name,
            vacancy.phone_numbers[0] if vacancy.phone_numbers else None,
            vacancy.phone_numbers[1] if len(vacancy.phone_numbers) >= 2 else None,
            vacancy.email,
            vacancy.salary,
            vacancy.description,
            vacancy.vacancy_link
        ])

    # Сохраняем книгу в буфер
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)  # Перемещаем указатель в начало буфера

    return buffer
