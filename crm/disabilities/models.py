from django.db import models

from patients.models import Patient


class Employer(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Место работы"
    )
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )

    class Meta:
        verbose_name = "Работодатель"
        verbose_name_plural = "Работодатели"
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(
        max_length=100, blank=True, verbose_name="Должность"
    )
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Disability(models.Model):
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name="disabilities",
        null=False,
        verbose_name="Работа",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="disabilities",
        null=False,
        verbose_name="Должность",
    )
    disability_start_date = models.DateField(
        null=True,
        default=None,
        blank=True,
        verbose_name="Дата начала больничного листа",
    )
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="disability",
        default=None,
        null=False,
        verbose_name="Пациент",
    )
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"
        ordering = ["disability_start_date"]

    def __str__(self):
        return self.disability_start_date.strftime("%d.%m.%Y")


class DisabilityCommissionDate(models.Model):
    date = models.DateField(
        null=True, blank=True, verbose_name="Дата ВК для ЭВН"
    )
    job = models.ForeignKey(
        Disability,
        on_delete=models.CASCADE,
        related_name="comission_dates",
        null=False,
        verbose_name="Нетрудоспособные",
    )
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )

    class Meta:
        verbose_name = "Дата ВК на ЭВН"
        verbose_name_plural = "Даты ВК на ЭВН"
        ordering = ["date"]

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")
