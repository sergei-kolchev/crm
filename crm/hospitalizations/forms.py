from django import forms
from django.utils import timezone

from .models import Hospitalization
from .utils import validate_hospitalization_fields


class CreateHospitalizationForm(forms.ModelForm):
    class Meta:
        model = Hospitalization
        fields = (
            "entry_date",
            "leaving_date",
            "patient",
            "doctor",
            "number",
            "involuntary",
            "diagnosis",
            "custom_diagnosis",
            "notes",
        )
        widgets = {
            "entry_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%d %H:%M",
            ),
            "leaving_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%d %H:%M",
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "patient": forms.Select(
                attrs={"class": "form-select", "size": 10}
            ),
            "doctor": forms.Select(attrs={"class": "form-select", "size": 4}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "diagnosis": forms.Select(attrs={"class": "form-select"}),
            "involuntary": forms.Select(attrs={"class": "form-select"}),
            "custom_diagnosis": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if "patient" in cleaned_data and "entry_date" in cleaned_data:
            hospitalizations = Hospitalization.objects.filter(
                patient__pk=cleaned_data["patient"].pk
            ).select_related("patient")
            validate_hospitalization_fields(cleaned_data, hospitalizations)
        return cleaned_data


class UpdateHospitalizationForm(forms.ModelForm):
    class Meta:
        model = Hospitalization
        fields = (
            "entry_date",
            "leaving_date",
            "patient",
            "doctor",
            "number",
            "involuntary",
            "diagnosis",
            "custom_diagnosis",
            "notes",
        )

        widgets = {
            "entry_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%d %H:%M",
            ),
            "leaving_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%d %H:%M",
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "patient": forms.Select(
                attrs={"class": "form-select", "size": 10}
            ),
            "doctor": forms.Select(attrs={"class": "form-select", "size": 4}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "diagnosis": forms.Select(attrs={"class": "form-select"}),
            "involuntary": forms.Select(attrs={"class": "form-select"}),
            "custom_diagnosis": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if "patient" in cleaned_data and "entry_date" in cleaned_data:
            hospitalizations = (
                Hospitalization.objects.filter(
                    patient__pk=cleaned_data["patient"].pk
                )
                .exclude(id=self.instance.id)
                .select_related("patient")
            )
            validate_hospitalization_fields(cleaned_data, hospitalizations)
        return cleaned_data


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Hospitalization
        fields = ["leaving_date"]

        widgets = {
            "leaving_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                    "value": timezone.now().strftime("%Y-%m-%d %H:%M"),
                },
                format="%Y-%m-%d %H:%M",
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.entry_date > cleaned_data["leaving_date"]:
            raise forms.ValidationError(
                "Дата поступления {} не может быть больше даты выписки".format(
                    self.instance.entry_date.strftime("%d.%m.%Y %H:%M")
                )
            )
        return cleaned_data


class UpdateHospitalizationInlineForm(forms.ModelForm):
    class Meta:
        model = Hospitalization
        fields = ["entry_date", "leaving_date", "notes"]

        widgets = {
            "entry_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%d %H:%M",
            ),
            "leaving_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%d %H:%M",
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Заметки"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if "entry_date" in cleaned_data:
            hospitalization = Hospitalization.objects.get(pk=self.instance.pk)
            h = hospitalization.patient.hospitalizations.exclude(
                pk=self.instance.pk
            )
            validate_hospitalization_fields(cleaned_data, h)
        return cleaned_data
