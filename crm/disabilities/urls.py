from django.urls import path

from disabilities import views

app_name = "disabilities"

urlpatterns = [
    path("", views.DisabilitiesList.as_view(), name='list'),
]
