from abc import ABC, abstractmethod
from typing import Callable, Union

from django.urls import reverse

from tables.buttons import Button
from tables.cells import Cell, TableBodyCell, TableButtonsCell, TableHeaderCell


class CellBuilder(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class TableHeaderCellBuilder(CellBuilder):
    @classmethod
    def __raw_params(cls, request_params: dict) -> str:
        return "&".join([f"{k}={v}" for k, v in request_params.items()])

    @classmethod
    def __reverse(
        cls,
        direction: str,
        kwargs: dict,
    ) -> str:
        params = kwargs["_request_kwargs"].copy()
        if "order" in params:
            params.pop("order")
            params.pop("direction")
        url = reverse(
            viewname=kwargs.get("_view_name_th"),
            kwargs={
                "order": kwargs.get("_name"),
                "direction": direction,
                **params,
            },
        )

        if "_request_params" in kwargs and kwargs["_request_params"]:
            url += f"?{cls.__raw_params(kwargs.get('_request_params'))}"

        return url

    def __add_sorting_url(self, kwargs) -> None:
        kwargs["_asc_sorting_url"] = self.__reverse("asc", kwargs)
        kwargs["_desc_sorting_url"] = self.__reverse("desc", kwargs)

    def __call__(self, **kwargs) -> TableHeaderCell:
        if "_view_name_th" in kwargs and kwargs["_view_name_th"]:
            self.__add_sorting_url(kwargs)
        return TableHeaderCell(**kwargs)


class TableBodyCellBuilder(CellBuilder):
    @staticmethod
    def __reverse(kwargs: dict) -> str:
        return reverse(
            viewname=kwargs.get("_view_name_td"),
            kwargs={
                "pk": kwargs.get("pk"),
            },
        )

    def _add_url(self, kwargs: dict) -> None:
        if "_view_name_td" in kwargs and kwargs["_view_name_td"]:
            kwargs["_url"] = self.__reverse(kwargs)

    @classmethod
    def _add_default_value(cls, kwargs: dict) -> None:
        if not kwargs.get("value") and kwargs.get("_default"):
            kwargs["value"] = kwargs["_default"]

    def __call__(self, **kwargs) -> TableBodyCell:
        self._add_url(kwargs)
        self._add_default_value(kwargs)
        return TableBodyCell(**kwargs)


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key: str, builder: Callable[..., Cell]):
        self._builders[key] = builder

    def create(
        self, key: str, **kwargs
    ) -> Union[TableBodyCell, TableHeaderCell]:
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(f"Unknown type of builder {key}")
        return builder(**kwargs)


class TableButtonsCellBuilder(CellBuilder):
    @classmethod
    def _check_buttons(cls, kwargs: dict) -> list[Button]:
        buttons = list(kwargs.get("buttons"))
        if not buttons:
            raise ValueError("Add at least one button")
        return buttons

    def __add_buttons(self, kwargs: dict) -> None:
        buttons = self._check_buttons(kwargs)
        for i in range(len(buttons)):
            buttons[i] = buttons[i].clone(pk=kwargs.get("pk"))
        kwargs["buttons"] = buttons

    def __call__(self, **kwargs) -> TableButtonsCell:
        self.__add_buttons(kwargs)
        return TableButtonsCell(**kwargs)
