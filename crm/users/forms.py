import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Логин"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.CharField(
        disabled=True,
        label="E-mail",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 5)),
            attrs={"class": "form-control"},
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "photo",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_birth",
        ]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "date_birth": "Дата рождения",
            "photo": "Аватарка",
        }
        widgets = {
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
