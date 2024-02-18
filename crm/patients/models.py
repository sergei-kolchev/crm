from django.db import models

from disabilities.models import Disability


class Patient(models.Model):
    class Incapacity(models.IntegerChoices):
        NO = 0, "нет"
        YES = 1, "да"

    name = models.CharField(max_length=100, db_index=True, verbose_name="Имя")
    surname = models.CharField(
        max_length=100, db_index=True, verbose_name="Фамилия"
    )
    patronymic = models.CharField(
        max_length=100, blank=True, db_index=True, verbose_name="Отчество"
    )
    birthday = models.DateField(verbose_name="Дата рождения")
    registration_address = models.TextField(
        blank=True, verbose_name="Адрес регистрации"
    )
    residential_address = models.TextField(
        blank=True, verbose_name="Адрес проживания"
    )
    incapacity = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Incapacity.choices)),
        default=Incapacity.NO,
        verbose_name="Недееспособность",
    )
    disability = models.OneToOneField(
        Disability,
        on_delete=models.SET_NULL,
        related_name="hospitalizations",
        default=None,
        null=True,
        verbose_name="Нетрудоспособность",
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="Статус")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["surname", "name", "patronymic", "birthday"],
                name="unique_patient",
            )
        ]
        ordering = ("surname",)
        indexes = [
            models.Index(fields=("surname", "name", "patronymic")),
            models.Index(fields=("time_create",)),
        ]
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        birthday = self.birthday.strftime("%d.%m.%Y")
        return f"{self.surname} {self.name} {self.patronymic}, {birthday} г.р."
