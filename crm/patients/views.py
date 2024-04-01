from typing import Union

from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import exceptions
from django.views.decorators.http import require_GET, require_http_methods
from htmx.http import HtmxHttpRequest, render_partial, require_HTMX
from utils.utils import login_required

from . import service
from .forms import AddPatientForm


@login_required
@require_GET
def index(request):
    return render_partial(
        request, "patients/main.html", context={"title": "CRM"}
    )


@login_required
@require_GET
def about(request):
    return render_partial(
        request, "patients/about.html", context={"title": "О проекте"}
    )


@login_required
@require_GET
def contacts(request):
    return render_partial(
        request, "patients/contacts.html", context={"title": "Контакты"}
    )


@login_required
@require_GET
def patient_list(
    request: HtmxHttpRequest | HttpRequest,
    order: str = "surname",
    direction: str = "asc",
) -> HttpResponse:
    search_query = request.GET.get("q")
    page_number = request.GET.get("page")

    page_obj = service.get_page(order, direction, page_number, search_query)
    form = AddPatientForm()
    return render_partial(
        request,
        template_name="patients/patient_list.html",
        context={
            "title": "Картотека пациентов",
            "patients": page_obj,
            "form": form,
            "order": order,
            "direction": direction,
            "q": search_query,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def create_patient(
    request: Union[HtmxHttpRequest, HttpRequest],
    order: str = "surname",
    direction: str = "asc",
) -> HttpResponse:
    message = None
    if request.method == "POST":
        form = AddPatientForm(request.POST)
        direction = request.POST.get("direction", direction)
        order = request.POST.get("order", order)
        if form.is_valid():
            form.save()
            message = "ok"
        else:
            message = "error"
    else:
        form = AddPatientForm()

    page_obj = service.get_page(order, direction)

    return render_partial(
        request,
        "patients/patient_list.html",
        context={
            "title": "Картотека пациентов",
            "patients": page_obj,
            "form": form,
            "order": order,
            "direction": direction,
        },
        message=message,
    )


@login_required
@require_HTMX("patients:index")
@require_http_methods(["POST", "PUT"])
def update_patient(request: HtmxHttpRequest, pk: int) -> HttpResponse:
    patient = service.get_one(pk)
    if request.method == "POST":
        form = AddPatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            return render_partial(
                request,
                "patients/includes/patient_detail.html",
                context={
                    "patient": patient,
                },
                message="ok",
            )
    form = AddPatientForm(instance=patient)
    return render_partial(
        request,
        "patients/includes/update_patient_form.html",
        context={
            "form": form,
            "patient": patient,
        },
    )


@login_required
@require_HTMX("patients:index")
@require_http_methods(["DELETE"])
def patient_delete(request: HtmxHttpRequest, pk: int) -> HttpResponse:
    patient = service.get_one(pk)
    patient.delete()
    return render_partial(
        request,
        "patients/includes/patient_deleted.html",
        message="ok",
    )


@login_required
@require_HTMX("patients:index")
@require_GET
def patient_detail(request: HtmxHttpRequest, pk: int) -> HttpResponse:
    patient = service.get_one(pk)
    return render(
        request,
        "patients/includes/patient_detail.html",
        context={
            "patient": patient,
        },
    )


@login_required
@require_HTMX("patients:index")
@require_http_methods(["POST", "PUT"])
def update_patient_status(request: HtmxHttpRequest, pk: int):
    patient = service.get_one(pk)
    patient.active = ~F("active")
    patient.save()
    patient.refresh_from_db(fields=["active"])

    return render(
        request,
        "patients/includes/patient_detail.html",
        context={
            "patient": patient,
        },
    )


@login_required
@require_HTMX("patients:index")
@require_http_methods(["GET"])
def search(request: HtmxHttpRequest) -> HttpResponse:
    search_query = request.GET.get("q")
    page_obj = service.get_page(search_query=search_query)

    return render(
        request,
        "patients/includes/patients_list_table.html",
        context={
            "patients": page_obj,
            "order": "surname",
            "direction": "asc",
            "q": search_query,
        },
    )


def page_not_found(
    request: HttpRequest, exception: exceptions.Resolver404
) -> HttpResponse:
    return render(
        request,
        template_name="patients/error.html",
        context={
            "title": "404",
            "content": "Страница не найдена",
        },
        status=404,
    )


def server_error(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        template_name="patients/error.html",
        context={
            "title": "500",
            "content": "Ошибка сервера",
        },
        status=500,
    )


def forbidden(request: HttpRequest, exception) -> HttpResponse:
    return render(
        request,
        template_name="patients/error.html",
        context={
            "title": "403",
            "content": "Доступ запрещен",
        },
        status=403,
    )
