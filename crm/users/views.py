from crm import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from utils.mixins import DataMixin
from utils.utils import LoginRequiredMixin

from .forms import LoginUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {
        "title": "Авторизация",
    }

    def get_success_url(self):
        return reverse_lazy("patients:index")


class ProfileUser(LoginRequiredMixin, DataMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {
        "title": "Профиль пользователя",
        "default_image": settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(LoginRequiredMixin, DataMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
