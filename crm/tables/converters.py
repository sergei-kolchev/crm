from abc import ABC, abstractmethod
from typing import Any


class Converter(ABC):
    message = "Error while converting data - {}"

    def __init__(self, message: str = "") -> None:
        if message:
            self.message = message

    @abstractmethod
    def convert(self, value: Any) -> Any:
        pass

    def __call__(self, value: Any, *args, **kwargs) -> Any:
        try:
            return self.convert(value)
        except ValueError as ex:
            raise ValueError(self.message.format(value) + str(ex))
        except Exception as ex:
            raise Exception(self.message.format(value) + str(ex))


class CellContentConverter:
    def __init__(self, converters: list[Converter] = None) -> None:
        self._converters = []
        if converters is not None:
            self._converters += converters

    def convert(self, value: Any) -> Any:
        for converter in self._converters:
            value = converter(value)
        return value
