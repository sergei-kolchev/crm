from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url

from htmx.http import HtmxResponseRedirect


def login_required(
    function=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME
):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)

        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = request.get_full_path()
        from django.contrib.auth.views import redirect_to_login

        # HTMX redirect
        if request.htmx:
            return HtmxResponseRedirect(resolved_login_url)

        return redirect_to_login(path, resolved_login_url, redirect_field_name)

    return wrap


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())

        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()

        # HTMX redirect
        if self.request.htmx:
            return HtmxResponseRedirect(resolved_login_url)
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )
