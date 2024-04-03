from typing import Any

from tables.converters import Converter


class FioConverter(Converter):
    def __init__(self):
        self.message = "Error while converting surname, name and patronymic "
        super().__init__()

    def convert(self, value: Any) -> Any:
        return str(value).split(",")[0]
