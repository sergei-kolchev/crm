# Generated by Django 5.0 on 2024-01-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospitalizations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hospitalization",
            name="notes",
            field=models.TextField(blank=True, verbose_name="Заметки"),
        ),
        migrations.DeleteModel(
            name="Note",
        ),
    ]