from django.contrib import admin
from django.urls import include, path
from patients import views

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("", include("patients.urls")),
]

handler403 = views.forbidden
handler404 = views.page_not_found
handler500 = views.server_error

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "CRM"
