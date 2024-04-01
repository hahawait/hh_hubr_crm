from pydantic import RootModel

from apps.base.models import VacancyModel


class HHResponce(RootModel):
    root: list[VacancyModel]
