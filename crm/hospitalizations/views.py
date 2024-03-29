from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from file_downloader.views import CreateFileDocxView
from htmx.http import RenderPartial
from patients import service as patient_service
from tables.views import TableInlineFormView, TableRowView, TableView
from utils.mixins import DataMixin
from utils.utils import LoginRequiredMixin

from . import service, tasks
from .forms import (
    CreateHospitalizationForm,
    LeaveForm,
    UpdateHospitalizationForm,
    UpdateHospitalizationInlineForm,
)
from .models import Hospitalization
from .tables import CurrentHospitalizationsTable, HospitalizationsTable


class HospitalizationsList(LoginRequiredMixin, DataMixin, TableView, ListView):
    model = Hospitalization
    template_name = "hospitalizations/hospitalizations_list.html"
    context_object_name = "hospitalizations"
    title_page = "Список госпитализаций"
    table_view_name = "hospitalizations:hospitalizations"
    table_schema = HospitalizationsTable

    def get_queryset(self):
        return service.get_all(patient_pk=self.kwargs["pk"], **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            order=self.kwargs.get("order", "entry_date"),
            direction=self.kwargs.get("direction", "asc"),
            patient=patient_service.get_one(self.kwargs["pk"]),
        )


class CurrentHospitalizationsList(
    LoginRequiredMixin, DataMixin, TableView, ListView
):
    model = Hospitalization
    template_name = "hospitalizations/current_hospitalizations_list.html"
    context_object_name = "hospitalizations"
    selected_doctor = 0
    title_page = "Находящиеся на лечении"
    table_view_name = "hospitalizations:current"
    table_schema = CurrentHospitalizationsTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            order=self.kwargs.get("order", "patient"),
            direction=self.kwargs.get("direction", "asc"),
            selected_doctor=self.selected_doctor,
            doctors=get_user_model().objects.all(),
        )

    def get_queryset(self):
        self.selected_doctor = int(self.request.GET.get("selected_doctor", 0))
        return service.get_all_current(self.selected_doctor, **self.kwargs)


class CreateHospitalization(LoginRequiredMixin, DataMixin, CreateView):
    form_class = CreateHospitalizationForm
    template_name = "hospitalizations/add_hospitalization.html"
    success_url = reverse_lazy("hospitalizations:current")
    title_page = "Добавление госпитализации"


class UpdateCurrentHospitalization(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = UpdateHospitalizationForm
    template_name = "hospitalizations/add_hospitalization.html"
    success_url = reverse_lazy("hospitalizations:current")
    title_page = "Редактирование госпитализации"
    allow_empty = False
    extra_context = {
        "update": True,
    }

    def get_queryset(self):
        return service.get(pk=self.kwargs["pk"])


class UpdateHospitalization(
    LoginRequiredMixin, DataMixin, TableInlineFormView, UpdateView
):
    form_class = UpdateHospitalizationInlineForm
    table_row_update_view = "hospitalizations:update"
    table_row_detail_view = "hospitalizations:detail"

    def get_queryset(self):
        return service.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        if "pk" in self.kwargs:
            hospitalization = service.get_one(pk=self.kwargs["pk"])
            return reverse(
                "hospitalizations:detail", kwargs={"pk": hospitalization.pk}
            )


class DeleteCurrentHospitalization(LoginRequiredMixin, DataMixin, DeleteView):
    model = Hospitalization
    success_url = reverse_lazy("hospitalizations:current")


class DeleteHospitalization(LoginRequiredMixin, DataMixin, DeleteView):
    model = Hospitalization

    def get_success_url(self):
        if "pk" in self.kwargs:
            hospitalization = service.get_one(pk=self.kwargs["pk"])
            pk = hospitalization.patient.pk
            h = hospitalization.patient.hospitalizations.all()
            if len(h) > 1:
                return reverse(
                    "hospitalizations:hospitalizations", kwargs={"pk": pk}
                )
            return reverse("patients:patients")


class Leave(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = LeaveForm
    template_name = "hospitalizations/leave.html"
    success_url = reverse_lazy("hospitalizations:current")
    title_page = "Выписать пациента"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            pk=self.kwargs["pk"],
            hospitalization=service.get_one(pk=self.kwargs["pk"]),
        )

    def get_queryset(self):
        return service.get(pk=self.kwargs["pk"])


class HospitalizationDetailView(
    LoginRequiredMixin, DataMixin, TableRowView, TemplateView
):
    allow_empty = False
    table_schema = HospitalizationsTable
    table_view_name = "hospitalizations:hospitalizations"

    def get_queryset(self):
        return service.get_one(pk=self.kwargs["pk"])


class CurrentHospitalizationsCreateDocxView(
    LoginRequiredMixin, RenderPartial, CreateFileDocxView
):
    template_file_path = "docx/list.docx"
    download_url = "hospitalizations:download_current_docx"
    task = tasks.BuildCurrentDocxFileTask  # TODO str?
    selected_doctor = 0

    def get(self, request, *args, **kwargs):
        self.selected_doctor = int(request.GET.get("selected_doctor", 0))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.task_kwargs = {
            "selected_doctor": self.selected_doctor,
            "order": self.kwargs.get("order", "surname"),
            "direction": self.kwargs.get("direction", "asc"),
        }
        context = super().get_context_data(**self.task_kwargs)
        return context


class CurrentHospitalizationsByDoctorsCreateDocxView(
    LoginRequiredMixin, RenderPartial, CreateFileDocxView
):
    template_file_path = "docx/list_by_doctors.docx"
    download_url = "hospitalizations:download_current_docx"
    task = tasks.BuildCurrentByDoctorsDocxFileTask  # TODO str?


class CurrentHospitalizationsCreateXlsxView(
    CurrentHospitalizationsCreateDocxView
):
    template_file_path = "docx/list.xlsx"
    temp_file_extension = "xlsx"
    download_url = "hospitalizations:download_current_xlsx"
    task = tasks.BuildCurrentXlsxFileTask  # TODO str? агрегация


class DocumentsView(LoginRequiredMixin, DataMixin, DetailView):
    model = Hospitalization
    template_name = "hospitalizations/documents.html"
    context_object_name = "hospitalization"
    title_page = "Документы"


class CreateDocumentDocxView(
    LoginRequiredMixin, RenderPartial, CreateFileDocxView
):
    download_url = "hospitalizations:download_docx"
    task = tasks.BuildDocxFileTask

    def get_context_data(self, **kwargs):
        self.task_kwargs = {
            "pk": self.kwargs.get("pk"),
        }
        context = super().get_context_data(**self.task_kwargs)
        return context


###


class CreateReferenceDocxView(CreateDocumentDocxView):
    template_file_path = "docx/reference.docx"


class CreateReferralDocxView(CreateDocumentDocxView):
    template_file_path = "docx/referral.docx"
    filename = "Направление"
