from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from patients import views

from crm import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("patients.urls")),
    path("users/", include("users.urls")),
    path("hospitalizations/", include("hospitalizations.urls")),
]

handler403 = views.forbidden
handler404 = views.page_not_found
handler500 = views.server_error

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "CRM"
