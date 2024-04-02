from pydantic import BaseModel


class ContactMemberModel(BaseModel):
    contact_name: str
    contacts: dict[str, str] = {}


class CompanyModel(BaseModel):
    company_name: str
    contacts: dict[str, str] = {}
    contact_members: list[ContactMemberModel] = []
