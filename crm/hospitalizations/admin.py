from django.contrib import admin
from hospitalizations.models import Diagnosis, Hospitalization


@admin.register(Hospitalization)
class HospitalizationAdmin(admin.ModelAdmin):
    list_display = ("patient", "entry_date", "leaving_date")


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ("diagnosis", "icd_code")
