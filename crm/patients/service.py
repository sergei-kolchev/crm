from typing import Any

from django.core.paginator import Page, Paginator

from crm import settings

from .models import Patient
from .utils import get_filtering_query


def get_page(
    order_by: Any = "surname",
    direction: Any = "asc",
    page_number: Any | None = None,
    search_query: Any | None = None,
) -> Page:
    patients = get_all(order_by, direction, search_query)
    paginator = Paginator(patients, settings.PATIENTS_PAGINATE_BY)
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_all(
    order_by: str = "surname",
    direction: str = "asc",
    search_query: str | None = None,
) -> list[Patient]:
    if direction == "desc":
        order_by = "-" + order_by
    if search_query:
        patients = Patient.objects.filter(
            *get_filtering_query(search_query)
        ).order_by(order_by)
    else:
        patients = Patient.objects.order_by(order_by)
    return patients
