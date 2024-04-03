from abc import ABC
from typing import Optional, Union

from tables.buttons import Button
from tables.html import HTMLAttributes


class Cell(ABC):
    pass


class BaseCell(Cell):
    def __init__(self, _visible: bool = True, **kwargs) -> None:
        self._visible = _visible

    @property
    def visible(self):
        return self._visible

    def to_dict(self):
        res = {}
        for key, value in vars(self).items():
            if "__" not in key:
                if key.startswith("_"):
                    key = key[1:]
                res[key] = value
        return res


class TableHeaderCell(BaseCell):
    def __init__(
        self,
        _name: str,
        _verbose_name: str = "",
        _attrs_th: Optional[HTMLAttributes] = None,
        _asc_sorting_url: Optional[str] = None,
        _desc_sorting_url: Optional[str] = None,
        **kwargs
    ) -> None:
        self._name = _verbose_name or _name.title()
        self._sorting_field = _name
        if _attrs_th:
            self._attrs = _attrs_th.raw
        else:
            self._attrs = None
        self._asc_sorting_url = _asc_sorting_url
        self._desc_sorting_url = _desc_sorting_url
        super().__init__(**kwargs)

    @property
    def name(self):
        return self._name

    @property
    def sorting_field(self):
        return self._sorting_field

    @property
    def attrs(self):
        return self._attrs

    @property
    def asc_sorting_url(self):
        return self._asc_sorting_url

    @property
    def desc_sorting_url(self):
        return self._desc_sorting_url


class TableBodyCell(BaseCell):
    def __init__(
        self,
        pk: Optional[int] = None,
        value: str = "",
        _url: Optional[str] = None,
        _attrs_td: Optional[HTMLAttributes] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._attrs = _attrs_td
        self._pk = pk
        self._url = _url
        self.value = value

    @property
    def attrs(self) -> HTMLAttributes:
        return self._attrs

    @property
    def url(self) -> str:
        return self._url


class Table:
    def __init__(self, table_id: Optional[str] = None) -> None:
        self.__validate_table_id(table_id)
        self.__table_id = table_id
        self.__header = []
        self.__body_rows = []

    @classmethod
    def __validate_table_id(cls, table_id: str) -> None:
        if table_id and type(table_id) is not str:
            raise TypeError("Expected str type for table_id")

    @property
    def header(self) -> list[TableHeaderCell]:
        return self.__header

    def add_cell_to_header(self, value: TableHeaderCell) -> None:
        if not isinstance(value, TableHeaderCell):
            raise TypeError("Expected HeaderField object")
        self.__header.append(value)

    @property
    def body_rows(self) -> list[list[TableBodyCell]]:
        return self.__body_rows

    def add_body_row(self, row: Union[list, tuple]) -> None:
        if type(row) not in [list, tuple]:
            raise TypeError("Expected list or tuple type for body row")
        self.__body_rows.append(row)

    @property
    def table_id(self) -> str:
        return self.__table_id

    @table_id.setter
    def table_id(self, value: str) -> None:
        self.__validate_table_id(value)
        self.__table_id = value


class TableButtonsCell(BaseCell):
    cell_type = "buttons"

    def __init__(
        self,
        *,
        pk: int,
        buttons: list[Button],
        _attrs_td: Optional[HTMLAttributes] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        if not pk or type(pk) is not int:
            raise TypeError(
                'Expected int type for "pk", attribute "pk" cant\'t '
                "be empty or None type"
            )
        self._pk = pk
        self.buttons = buttons
        self._attrs = _attrs_td

    @property
    def attrs(self) -> HTMLAttributes:
        return self._attrs
