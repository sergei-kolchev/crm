# Generated by Django 5.0 on 2024-02-13 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospitalizations", "0004_alter_hospitalization_involuntary"),
        ("medical_cards", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medicalcard",
            name="diagnosis",
        ),
        migrations.AlterField(
            model_name="hospitalization",
            name="medical_card",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="hospitalization",
                to="medical_cards.medicalcard",
                verbose_name="Медицинская карта",
            ),
        ),
        migrations.DeleteModel(
            name="Diagnosis",
        ),
        migrations.DeleteModel(
            name="MedicalCard",
        ),
    ]
