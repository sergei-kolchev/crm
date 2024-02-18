from django.views.generic import ListView

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
