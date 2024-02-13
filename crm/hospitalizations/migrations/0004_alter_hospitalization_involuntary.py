# Generated by Django 5.0 on 2024-01-30 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "hospitalizations",
            "0003_disability_hospitalization_involuntary_diagnosis_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="hospitalization",
            name="involuntary",
            field=models.BooleanField(
                choices=[(False, "нет"), (True, "да")],
                default=0,
                verbose_name="Недобровольная госпитализация",
            ),
        ),
    ]