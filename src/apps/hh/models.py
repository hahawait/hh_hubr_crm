from pydantic import BaseModel, validator


class VacancyModel(BaseModel):
    company_name: str | None = None
    vacancy_name: str | None = None
    phone_numbers: list[str] | None = None
    email: str | None = None
    contact_name: str | None = None
    salary: str | None = None
    description: str | None = None
    vacancy_link: str | None = None

    @validator('phone_numbers', pre=True)
    def remove_tel_prefix(cls, v):
        if v:
            return [phone.replace('tel:', '') for phone in v]
        return v
