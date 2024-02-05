from django.contrib import admin
from hospitalizations.models import Hospitalization


@admin.register(Hospitalization)
class HospitalizationAdmin(admin.ModelAdmin):
    list_display = ("patient", "entry_date", "leaving_date")
