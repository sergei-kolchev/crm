import datetime

from django import forms

from .models import Patient


class AddPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        this_year = datetime.date.today().year
        fields = ("surname", "name", "patronymic", "birthday")
        labels = {
            "surname": "Фамилия",
            "name": "Имя",
            "patronymic": "Отчество",
            "birthday": "Дата рождения",
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
            "patronymic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Отчество"}
            ),
        }
