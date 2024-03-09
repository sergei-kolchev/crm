import datetime

from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from disabilities import models
from disabilities.models import Disability, DisabilityCommissionDate
from patients.models import Patient


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


DisabilityFormset = inlineformset_factory(Patient, Disability, fields=['disability_start_date', 'patient', 'employer', 'position'], extra=1)
DisabilityCommissionDate = inlineformset_factory(Disability, DisabilityCommissionDate, fields=['date'], extra=5)


class BaseFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseFormset, self).add_fields(form, index)

        form.nested = DisabilityCommissionDate(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            #extra=1
        )


Formset = inlineformset_factory(models.Patient,
                                models.Disability,
                                fields=['disability_start_date', 'patient', 'employer', 'position'],
                                formset=BaseFormset,
                                extra=1)
