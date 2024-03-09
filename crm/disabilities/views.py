from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from disabilities.forms import CreateDisabilityForm, Formset
from disabilities.models import Disability
from disabilities.tables import DisabilityTable
from tables.views import TableView
from utils.mixins import DataMixin
from utils.utils import LoginRequiredMixin


class DisabilitiesList(
    LoginRequiredMixin, DataMixin, TableView, ListView
):
    model = Disability
    template_name = "disabilities/list.html"
    context_object_name = "disabilities"
    title_page = "Нетрудоспособные"
    table_view_name = "disabilities:list"
    table_schema = DisabilityTable

    def get_queryset(self):
        return Disability.objects.all()


class CreateDisability(
    LoginRequiredMixin, DataMixin, CreateView
):
    #form_class = CreateDisabilityForm
    form_class = Formset
    #from_class = BookImageFormset
    template_name = "disabilities/add.html"
    success_url = reverse_lazy("disabilities:list")
    title_page = "Добавление периода нетрудоспособности"
    #fields = ('patient', 'employer', 'position')

    def get_queryset(self):
        print(self.from_class)
        return Disability.objects.all()
