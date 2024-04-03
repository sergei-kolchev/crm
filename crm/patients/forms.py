import datetime

from django import forms

from .models import Patient


class AddPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        this_year = datetime.date.today().year
        fields = (
            "surname",
            "name",
            "patronymic",
            "birthday",
            "registration_address",
            "residential_address",
        )
        labels = {
            "surname": "Фамилия",
            "name": "Имя",
            "patronymic": "Отчество",
            "birthday": "Дата рождения",
            "registration_address": "Адрес регистрации",
            "residential_address": "Адрес проживания",
        }
        widgets = {
            "birthday": forms.SelectDateWidget(
                empty_label=("Год", "Месяц", "День"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Дата рождения",
                },
                years=tuple(range(this_year - 100, this_year - 5)),
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Фамилия"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "registration_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Адрес регистрации",
                }
            ),
            "residential_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Адрес проживания",
                }
            ),
            "patronymic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Отчество"}
            ),
        }
