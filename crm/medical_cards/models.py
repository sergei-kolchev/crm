from django.db import models

from hospitalizations.models import Hospitalization


class Diagnosis(models.Model):
    diagnosis = models.TextField(
        blank=True, unique=True, verbose_name="Диагноз"
    )
    icd_code = models.CharField(
        max_length=10,
        blank=True,
        unique=True,
        verbose_name="Код диагноза по МКБ-10",
    )

    class Meta:
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"
        ordering = ["diagnosis"]

        indexes = [
            models.Index(fields=["icd_code"]),
            models.Index(fields=["diagnosis"]),
        ]

    def __str__(self):
        return self.icd_code


class MedicalCard(models.Model):
    number = models.CharField(
        max_length=15, verbose_name="Номер медицинской карты"
    )
    diagnosis = models.ManyToManyField(
        Diagnosis,
        blank=True,
        related_name="medical_cards",
        verbose_name="Диагнозы",
    )
    custom_diagnosis = models.TextField(
        blank=True, verbose_name="Диагноз"
    )
    hospitalization = models.OneToOneField(
        Hospitalization,
        on_delete=models.PROTECT,
        related_name="medical_card",
        verbose_name="Госпитализация",
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = "Медицинская карта"
        verbose_name_plural = "Медицинские карты"
        ordering = ["number"]

        indexes = [
            models.Index(fields=["number"]),
        ]

    def __str__(self):
        return self.number
