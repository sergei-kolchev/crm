from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from patients.models import Patient


class Diagnosis(models.Model):
    diagnosis = models.TextField(unique=True, verbose_name="Диагноз")
    icd_code = models.CharField(
        max_length=10,
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


class NowInDepartmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(leaving_date=None)


class Hospitalization(models.Model):
    class Involuntary(models.IntegerChoices):
        NO = 0, "нет"
        YES = 1, "да"

    entry_date = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name="Дата поступления"
    )
    leaving_date = models.DateTimeField(
        null=True,
        default=None,
        blank=True,
        db_index=True,
        verbose_name="Дата выписки",
    )
    involuntary = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Involuntary.choices)),
        default=Involuntary.NO,
        verbose_name="Недобровольная госпитализация",
    )
    notes = models.TextField(blank=True, verbose_name="Заметки")
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="hospitalizations",
        null=False,
        verbose_name="Пациент",
    )
    doctor = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="hospitalizations",
        null=True,
        default=None,
        verbose_name="Лечащий врач",
    )
    number = models.CharField(
        max_length=15, verbose_name="Номер медицинской карты"
    )
    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.SET_NULL,
        null=True,
        related_name="medical_cards",
        verbose_name="Диагноз",
    )
    custom_diagnosis = models.TextField(blank=True, verbose_name="Диагноз")
    objects = models.Manager()
    current = NowInDepartmentManager()

    class Meta:
        verbose_name = "Госпитализация"
        verbose_name_plural = "Госпитализации"
        ordering = ["patient__surname"]
        constraints = [
            models.UniqueConstraint(
                fields=["entry_date", "patient"], name="unique_hospitalization"
            )
        ]
        indexes = [
            models.Index(fields=["leaving_date"]),
            models.Index(fields=["-entry_date"]),
        ]

    def __str__(self):
        return "{} - {}".format(
            self.entry_date.strftime("%d.%m.%Y"),
            self.leaving_date.strftime("%d.%m.%Y")
            if self.leaving_date
            else "находится в отделении",
        )
