from datetime import datetime

from pydantic import BaseModel


class VacancyModel(BaseModel):
    company_name: str | None = None
    vacancy_name: str | None = None
    salary: str | None = None
    date: datetime | None = None


class CompanyContactMemberModel(BaseModel):
    contact_name: str
    contacts: dict[str, str] = {}


class CompanyContactMembersModel(BaseModel):
    company_name: str
    contact_members: list[CompanyContactMemberModel] = []


class CompanyModel(BaseModel):
    company_name: str
    contacts: dict[str, str] = {}
