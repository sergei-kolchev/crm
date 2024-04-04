from typing import Optional, Union

from django.db.models import QuerySet
from django.http import QueryDict

from tables import factory
from tables.cells import Table, TableBodyCell, TableHeaderCell
from tables.converters import CellContentConverter
from tables.fields import ButtonsField, Field


class TableSchema:
    _meta = None

    def __init__(
        self,
        view_name: str,
        request_params: Optional[QueryDict] = None,
        request_kwargs: Optional[dict] = None,
    ) -> None:
        self.__table = Table()
        if hasattr(self, "Meta"):
            self._meta = self.Meta()
        if request_params and type(request_params) is not QueryDict:
            raise TypeError(
                "The request_params argument must be of type dict."
            )
        self._request_params = request_params or {}
        self._request_kwargs = request_kwargs

        if not view_name:
            raise ValueError('"View_name" can\'t be an empty')
        self.__view_name = view_name

    @property
    def view_name(self) -> str:
        return self.__view_name

    @property
    def table(self) -> Table:
        return self.__table

    def _add_header_cell(self, header: TableHeaderCell) -> None:
        self.__table.add_cell_to_header(header)

    def _add_body_row(
        self, row: Union[list[TableBodyCell], tuple[TableBodyCell]]
    ) -> None:
        self.__table.add_body_row(row)

    def _get_attributes_list(self) -> list[str]:
        if not self._meta or self._meta and not hasattr(self._meta, "index"):
            attributes = []
            for attribute in dir(self):
                if not attribute.startswith("__"):
                    a = getattr(self, attribute, None)
                    if not callable(a) and isinstance(a, Field):
                        attributes.append(attribute)
            return attributes
        return getattr(self._meta, "index", None)

    @classmethod
    def _apply_converters(cls, value, converters):
        converters = CellContentConverter(converters)
        return converters.convert(value)

    def _create_table_data(self, queryset: QuerySet) -> Table:
        attributes_list = self._get_attributes_list()

        for attribute_name in attributes_list:
            field = getattr(self, attribute_name)
            kwargs = {
                "_request_params": self._request_params,
                "_request_kwargs": self._request_kwargs,
            }
            if not field.name:
                field.name = attribute_name
            if "order" not in kwargs["_request_kwargs"]:
                kwargs["_request_kwargs"]["direction"] = "asc"
                kwargs["_request_kwargs"]["order"] = field.name
            kwargs.update(field.to_dict())
            self._add_header_cell(factory.create("header_cell", **kwargs))
        for obj in queryset:
            pk = getattr(obj, "pk", None)
            row = []
            for attribute in attributes_list:
                field = getattr(self, attribute)
                kwargs = {"pk": pk}
                kwargs.update(field.to_dict())
                if isinstance(field, ButtonsField):
                    kwargs["buttons"] = field.buttons
                    cell = factory.create("buttons_cell", **kwargs)
                else:
                    value = getattr(obj, attribute)
                    converters = field.converters
                    if converters:
                        value = self._apply_converters(value, converters)
                    kwargs["value"] = value
                    cell = factory.create("body_cell", **kwargs)
                row.append(cell)
            self._add_body_row(row)

        return self.table

    def get_body_row(self, obj):
        attributes_list = self._get_attributes_list()
        pk = getattr(obj, "pk", None)
        row = []
        for attribute in attributes_list:
            field = getattr(self, attribute)
            kwargs = {"pk": pk}
            kwargs.update(field.to_dict())
            if isinstance(field, ButtonsField):
                kwargs["buttons"] = field.buttons
                cell = factory.create("buttons_cell", **kwargs)
            else:
                value = getattr(obj, attribute)
                converters = field.converters
                if converters:
                    value = self._apply_converters(value, converters)
                kwargs["value"] = value
                cell = factory.create("body_cell", **kwargs)
            row.append(cell)
        return row

    def make_table(self, queryset: QuerySet) -> Table:
        return self._create_table_data(queryset)
