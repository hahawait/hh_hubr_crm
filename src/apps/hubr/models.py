from datetime import datetime

from pydantic import BaseModel, computed_field


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


class CompanyContactMembersUrlsModel(BaseModel): 
    company_name: str
    contact_members_urls: list[str] = []

    @computed_field
    @property
    def total_urls(self) -> int:
        return len(self.contact_members_urls)

class CompanyModel(BaseModel):
    company_name: str
    contacts: dict[str, str] = {}
