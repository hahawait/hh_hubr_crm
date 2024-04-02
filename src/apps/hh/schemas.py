from pydantic import RootModel

from apps.hh.models import VacancyModel


class HHResponce(RootModel):
    root: list[VacancyModel]
