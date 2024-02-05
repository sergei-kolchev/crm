import os
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToAndRename:
    def __init__(self, path):
        self.__path = path

    def __call__(self, instance, filename):
        extension = filename.split(".")[-1]
        if instance.pk:
            filename = f"{instance.pk}.{extension}"
        else:
            filename = f"{uuid4().hex}.{extension}"
        return os.path.join(self.__path, filename)


@deconstructible
class ImageMinDimValidator:
    _code = "image_min_dim_validator"

    def __init__(self, dims: tuple[int, int], message: str = None):
        if type(dims) is not tuple:
            raise TypeError('Invalid type of "dims" variable, tuple expected')

        if (
            len(dims) != 2
            or type(dims[0]) is not int
            or type(dims[1]) is not int
        ):
            raise ValueError(
                'Invalid value of "dims" variable, [int, int] expected'
            )

        if message and type(message) is not str:
            raise TypeError(
                'Invalid value of "message" variable, str expected'
            )

        self.__dims = dims
        self.__message = (
            message
            if message
            else (
                f"Размер изображения не должен быть меньше, "
                f"чем {self.__dims[0]}x{self.__dims[1]}"
            )
        )

    def __call__(self, img):
        width = img.width
        height = img.height
        if width < self.__dims[0] or height < self.__dims[1]:
            raise ValidationError(
                self.__message, code=self._code, params={"img": img}
            )


@deconstructible
class ImageMaxDimValidator:
    _code = "image_max_dim_validator"

    def __init__(self, dims: tuple[int, int], message: str = None):
        if type(dims) is not tuple:
            raise TypeError('Invalid type of "dims" variable, tuple expected')

        if (
            len(dims) != 2
            or type(dims[0]) is not int
            or type(dims[1]) is not int
        ):
            raise ValueError(
                'Invalid value of "dims" variable, [int, int] expected'
            )

        if message and type(message) is str:
            raise TypeError(
                'Invalid value of "message" variable, str expected'
            )

        self.__dims = dims
        self.__message = (
            message
            if message
            else (
                f"Размер изображения не должен превышать "
                f"{self.__dims[0]}x{self.__dims[1]}"
            )
        )

    def __call__(self, img):
        width = img.width
        height = img.height
        if width > self.__dims[0] or height > self.__dims[1]:
            raise ValidationError(
                self.__message, code=self._code, params={"img": img}
            )


@deconstructible
class ImageSizeValidator:
    _code = "image_size_validator"

    def __init__(self, size: int, message: str = None):
        if type(size) is not int:
            raise TypeError('Invalid type of "size" variable, int expected')

        if message and type(message) is not str:
            raise TypeError(
                'Invalid value of "message" variable, str expected'
            )

        self.__size = size
        self.__message = (
            message
            if message
            else (
                f"Размер файла изображения не должен превышать "
                f"{round(self.__size/1000)} Kb"
            )
        )

    def __call__(self, img):
        size = img.size
        if size > self.__size:
            raise ValidationError(
                self.__message, code=self._code, params={"img": img}
            )


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = (
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгд"
        "еёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
    )
    code = "russian"

    def __init__(self, message=None):
        self.message = (
            message
            if message
            else "Должны присутствовать только русские символы, дефис и пробел"
        )

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, self.code)
