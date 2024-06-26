# Generated by Django 5.0 on 2024-01-04 12:16

from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_first_name_alter_user_last_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="patronymic",
            field=models.CharField(
                blank=True,
                max_length=150,
                validators=[users.validators.RussianValidator()],
                verbose_name="patronymic",
            ),
        ),
    ]
