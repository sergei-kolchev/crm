from django.urls import path

from hospitalizations import views
from utils import views as files_views

app_name = "hospitalizations"

urlpatterns = [
    path(
        "current/", views.CurrentHospitalizationsList.as_view(), name="current"
    ),
    path(
        "current/sort/<str:order>/<str:direction>/",
        views.CurrentHospitalizationsList.as_view(),
        name="current",
    ),
    path(
        "current/<int:pk>/update/",
        views.UpdateCurrentHospitalization.as_view(),
        name="update_current",
    ),
    path(
        "current/<int:pk>/delete/",
        views.DeleteCurrentHospitalization.as_view(),
        name="delete_current",
    ),
    path("current/<int:pk>/leave/", views.Leave.as_view(), name="leave"),
    path(
        "<int:pk>/",
        views.HospitalizationsList.as_view(),
        name="hospitalizations",
    ),
    path(
        "<int:pk>/sort/<str:order>/<str:direction>/",
        views.HospitalizationsList.as_view(),
        name="hospitalizations",
    ),
    path("add/", views.CreateHospitalization.as_view(), name="create"),
    path(
        "<int:pk>/delete/",
        views.DeleteHospitalization.as_view(),
        name="delete",
    ),
    path(
        "<int:pk>/update/",
        views.UpdateHospitalization.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/detail/",
        views.HospitalizationDetailView.as_view(),
        name="detail",
    ),
    path(
        "current/<str:order>/<str:direction>/docx",
        views.CurrentHospitalizationsCreateDocxView.as_view(),
        name="create_current_docx",
    ),
    path(
        "current/<str:order>/<str:direction>/xlsx",
        views.CurrentHospitalizationsCreateXlsxView.as_view(),
        name="create_current_xlsx",
    ),
    path(
        "tasks/<str:task_id>/status/",
        files_views.TaskStatusAuthorizedView.as_view(),
        name="task_status",
    ),
    path(
        "current/download/docx/<str:task_id>/",
        files_views.DownloadFileDocxAuthorizedView.as_view(filename="list"),
        name="download_current_docx",
    ),
    path(
        "current/doctors/docx",
        views.CurrentHospitalizationsByDoctorsCreateDocxView.as_view(),
        name="create_current_by_doctor_docx",
    ),
    path(
        "current/download/xlsx/<str:task_id>/",
        files_views.DownloadFileXlsxAuthorizedView.as_view(),
        name="download_current_xlsx",
    ),
    path(
        "documents/<int:pk>/",
        views.DocumentsView.as_view(),
        name="documents",
    ),
    path(
        "documents/download/docx/<str:task_id>/",
        files_views.DownloadFileDocxView.as_view(),
        name="download_docx",
    ),
    ###
    path(
        "documents/reference/<int:pk>/docx",
        views.CreateReferenceDocxView.as_view(),
        name="create_reference",
    ),
    path(
        "documents/referral/<int:pk>/docx",
        views.CreateReferralDocxView.as_view(),
        name="create_referral",
    ),
]
