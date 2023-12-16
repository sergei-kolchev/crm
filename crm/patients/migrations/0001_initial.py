# Generated by Django 5.0 on 2023-12-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("surname", models.CharField(db_index=True, max_length=100)),
                (
                    "patronymic",
                    models.CharField(
                        blank=True, db_index=True, max_length=100
                    ),
                ),
                ("birthday", models.DateField()),
                ("time_create", models.DateTimeField(auto_now_add=True)),
                ("time_update", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("surname",),
                "indexes": [
                    models.Index(
                        fields=["surname", "name", "patronymic"],
                        name="patients_pa_surname_8ab607_idx",
                    ),
                    models.Index(
                        fields=["time_create"],
                        name="patients_pa_time_cr_6212d5_idx",
                    ),
                ],
            },
        ),
    ]
