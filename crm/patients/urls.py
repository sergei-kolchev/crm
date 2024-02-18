from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.contacts, name="contacts"),
    path("about/", views.about, name="about"),
    path("patients/", views.patient_list, name="patients"),
    path("create/", views.create_patient, name="create_patient"),
    path("<int:pk>/delete/", views.patient_delete, name="patient_delete"),
    path("<int:pk>/update/", views.update_patient, name="update_patient"),
    path("<int:pk>/detail/", views.patient_detail, name="patient_detail"),
    path(
        "<int:pk>/status/",
        views.update_patient_status,
        name="update_patient_status",
    ),
    path(
        "patients/sort/<str:order>/<str:direction>/",
        views.patient_list,
        name="patients",
    ),
    path("patients/search/", views.search, name="search"),
]
