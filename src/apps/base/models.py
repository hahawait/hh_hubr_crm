from pydantic import BaseModel


class VacancyModel(BaseModel):
    company_name: str | None = None
    vacancy_name: str | None = None
    phone_numbers: list[str] | None = None
    email: str | None = None
    contact_name: str | None = None
    salary: int | None = None