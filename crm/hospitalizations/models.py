from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from patients.models import Patient

"""
Больничные листы
"""


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


"""
Медицинская карта
"""


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
        max_length=15, blank=True, verbose_name="Номер медицинской карты"
    )
    diagnosis = models.ManyToManyField(
        Diagnosis,
        blank=True,
        related_name="hospitalizations",
        verbose_name="Диагнозы",
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
    disability = models.OneToOneField(
        Disability,
        on_delete=models.SET_NULL,
        related_name="hospitalizations",
        default=None,
        null=True,
        verbose_name="Нетрудоспособность",
    )
    medical_card = models.OneToOneField(
        MedicalCard,
        on_delete=models.PROTECT,
        related_name="hospitalization",
        verbose_name="Медицинская карта",
        null=True,
        default=None,
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
        return "{}-{}".format(self.entry_date, self.leaving_date)
