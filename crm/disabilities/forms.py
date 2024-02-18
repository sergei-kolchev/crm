import datetime

from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from disabilities import models
from disabilities.models import Disability, DisabilityCommissionDate


class CreateDisabilityForm(forms.ModelForm):
    class Meta:
        model = Disability
        this_year = datetime.date.today().year
        fields = (
            'patient',
            'employer',
            'position',
            'disability_start_date',
        )

        widgets = {
            "disability_start_date": forms.SelectDateWidget(
                empty_label=("Год", "Месяц", "День"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Начало нетрудоспособности",
                },
                years=tuple(range(this_year - 100, this_year - 5)),
            ),
            "employer": forms.Select(
                attrs={"class": "form-select", "placeholder": "Работодатель"}
            ),
            "position": forms.Select(
                attrs={"class": "form-select", "placeholder": "Должность"}
            ),
            "patient": forms.Select(
                attrs={"class": "form-select", "placeholder": "Пациент"}
            ),
        }


class BaseCommissionDatesFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        #form.fields["disability_start_date"] = forms.DateTimeInput()

        form.nested = CreateDisabilityForm(
            instance=form.instance,
            data=form.data if form.is_bound else None,
        )


CommissionDatesFormset = inlineformset_factory(
    models.Disability,
    models.DisabilityCommissionDate,
    formset=BaseCommissionDatesFormset,
    fields=['date'],
    extra=1
)


BookImageFormset = inlineformset_factory(
    Disability, DisabilityCommissionDate, fields=['date', ]
)
