# Generated by Django 5.0 on 2024-02-13 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Diagnosis",
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
                (
                    "diagnosis",
                    models.TextField(blank=True, unique=True, verbose_name="Диагноз"),
                ),
                (
                    "icd_code",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        unique=True,
                        verbose_name="Код диагноза по МКБ-10",
                    ),
                ),
            ],
            options={
                "verbose_name": "Диагноз",
                "verbose_name_plural": "Диагнозы",
                "ordering": ["diagnosis"],
                "indexes": [
                    models.Index(
                        fields=["icd_code"], name="medical_car_icd_cod_82ac51_idx"
                    ),
                    models.Index(
                        fields=["diagnosis"], name="medical_car_diagnos_98ae16_idx"
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="MedicalCard",
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
                (
                    "number",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        verbose_name="Номер медицинской карты",
                    ),
                ),
                (
                    "custom_diagnosis",
                    models.TextField(blank=True, verbose_name="Диагноз"),
                ),
                (
                    "diagnosis",
                    models.ManyToManyField(
                        blank=True,
                        related_name="hospitalizations",
                        to="medical_cards.diagnosis",
                        verbose_name="Диагнозы",
                    ),
                ),
            ],
            options={
                "verbose_name": "Медицинская карта",
                "verbose_name_plural": "Медицинские карты",
                "ordering": ["number"],
                "indexes": [
                    models.Index(
                        fields=["number"], name="medical_car_number_8f4ff7_idx"
                    )
                ],
            },
        ),
    ]
