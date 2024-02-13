from django.urls import path

from medical_cards import views

app_name = "medical_cards"


urlpatterns = [
    path("", views.MedicalCardsList.as_view(), name="cards"),
    path("create/", views.CreateMedicalCard.as_view(), name="create"),
    path("<int:pk>/update/", views.UpdateMedicalCard.as_view(), name="update"),
    path("<int:pk>/delete/", views.DeleteMedicalCard.as_view(), name="delete"),
    path("<int:pk>/detail/", views.DetailMedicalCard.as_view(), name="detail"),
]
