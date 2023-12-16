from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    surname = models.CharField(max_length=100, db_index=True)
    patronymic = models.CharField(max_length=100, blank=True, db_index=True)
    birthday = models.DateField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("surname",)
        indexes = [
            models.Index(fields=("surname", "name", "patronymic")),
            models.Index(fields=("time_create",)),
        ]

    def __str__(self):
        return f"{self.surname}, {self.name}"
