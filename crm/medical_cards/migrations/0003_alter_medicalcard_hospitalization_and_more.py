# Generated by Django 5.0 on 2024-02-15 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospitalizations", "0006_remove_hospitalization_medical_card"),
        ("medical_cards", "0002_medicalcard_hospitalization_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicalcard",
            name="hospitalization",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="medical_card",
                to="hospitalizations.hospitalization",
                verbose_name="Госпитализация",
            ),
        ),
        migrations.AlterField(
            model_name="medicalcard",
            name="number",
            field=models.CharField(
                max_length=15, verbose_name="Номер медицинской карты"
            ),
        ),
    ]
