import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField

from crm import settings

from . import validators


class User(AbstractUser):
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        validators=[
            validators.RussianValidator(),
        ],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        validators=[
            validators.RussianValidator(),
        ],
    )
    patronymic = models.CharField(
        _("patronymic"),
        max_length=150,
        blank=True,
        validators=[
            validators.RussianValidator(),
        ],
    )
    photo = ThumbnailerImageField(
        upload_to=validators.UploadToAndRename(
            os.path.join("users/", "avatars")
        ),
        blank=True,
        null=True,
        resize_source=dict(
            size=(settings.AVATAR_WIDTH, settings.AVATAR_HEIGHT),
            sharpen=True,
            crop="smart",
            center=True,
            quality=99,
            upscale=True,
        ),
        verbose_name="Фотография",
        validators=[
            validators.ImageMinDimValidator(
                (
                    settings.AVATAR_MIN_WIDTH,
                    settings.AVATAR_MIN_HEIGHT,
                )
            ),
            validators.ImageMaxDimValidator(
                (
                    settings.AVATAR_MAX_WIDTH,
                    settings.AVATAR_MAX_HEIGHT,
                )
            ),
            validators.ImageSizeValidator(settings.AVATAR_FILE_MAX_SIZE),
        ],
    )
    date_birth = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата рождения"
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
