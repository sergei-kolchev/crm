from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from medical_cards.forms import CreateMedicalCardForm
from medical_cards.models import MedicalCard
from utils.mixins import DataMixin
from utils.utils import LoginRequiredMixin


class MedicalCardsList(LoginRequiredMixin, DataMixin, ListView):
    template_name = "medical_cards/list.html"
    title_page = "Медицинские карты"

    def get_queryset(self):
        return MedicalCard.objects.all()


class CreateMedicalCard(LoginRequiredMixin, DataMixin, CreateView):
    form_class = CreateMedicalCardForm
    template_name = "medical_cards/add.html"
    title_page = "Добавление медицинской карты"


class UpdateMedicalCard(LoginRequiredMixin, DataMixin, UpdateView):
    template_name = "medical_cards/update.html"
    title_page = "Обновление медицинской карты"


class DeleteMedicalCard(LoginRequiredMixin, DataMixin, DeleteView):
    pass


class DetailMedicalCard(LoginRequiredMixin, DataMixin, DetailView):
    template_name = "medical_cards/detail.html"
    title_page = "Медицинская карта"
