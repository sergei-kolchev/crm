from abc import ABC, abstractmethod
from types import NoneType
from typing import Optional

from tables.buttons import Button
from tables.html import HTMLAttributes


class Field(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass


class BaseField(Field):
    _allowed = {
        "_name": (str,),
        "_verbose_name": (str,),
        "_visible": (bool,),
        "_attrs_th": (HTMLAttributes, NoneType),
        "_attrs_td": (HTMLAttributes, NoneType),
        "_converters": (tuple, NoneType),
    }

    def __init__(
        self,
        name: str = "",
        verbose_name: str = "",
        visible: bool = True,
        attrs_th: Optional[HTMLAttributes] = None,
        attrs_td: Optional[HTMLAttributes] = None,
        converters: Optional[tuple] = None,
    ) -> None:
        self._name = name
        self._verbose_name = verbose_name
        self._visible = visible
        self._attrs_th = attrs_th
        self._attrs_td = attrs_td
        self._converters = converters

    def __setattr__(self, key, value):
        if key in self._allowed and type(value) not in self._allowed[key]:
            raise TypeError(f'Expected {self._allowed[key]} types for "{key}"')
        super().__setattr__(key, value)

    def __getattr__(self, item):
        raise AttributeError(f'Invalid attribute name "{item}"')

    def __delattr__(self, item):
        raise AttributeError(f'Unable to remove attribute "{item}"')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def verbose_name(self) -> str:
        return self._verbose_name

    @property
    def visible(self) -> bool:
        return self._visible

    @property
    def attrs_th(self) -> HTMLAttributes:
        return self._attrs_th

    @property
    def attrs_td(self) -> HTMLAttributes:
        return self._attrs_td

    @property
    def converters(self) -> tuple:
        return self._converters

    def to_dict(self) -> dict:
        return vars(self)


class TextField(BaseField):
    _allowed = {"_default": (str, NoneType), **BaseField._allowed}

    def __init__(self, default: Optional[str] = None, **kwargs) -> None:
        self._default = default
        super().__init__(**kwargs)


class TextSortedField(TextField):
    _allowed = {"_view_name_th": (str, NoneType), **TextField._allowed}

    def __init__(self, view_name_th: Optional[str] = None, **kwargs) -> None:
        self._view_name_th = view_name_th
        super().__init__(**kwargs)


class LinkField(TextField):
    _allowed = {
        "_view_name_td": (str, NoneType),
        **TextField._allowed,
    }

    def __init__(self, view_name_td: Optional[str] = None, **kwargs) -> None:
        self._view_name_td = view_name_td
        super().__init__(**kwargs)


class TextLinkSortedField(LinkField, TextSortedField):
    pass


class ButtonsField(BaseField):
    _allowed = {
        "_pk": (str,),
        "_buttons": (list,),
        **BaseField._allowed,
    }

    @classmethod
    def __check(cls, buttons: list[Button]) -> None:
        if not all(map(lambda button: isinstance(button, Button), buttons)):
            raise TypeError(
                'Expected type is "Button" for all buttons in the list.'
            )

    def __init__(self, buttons: list[Button], **kwargs) -> None:
        self.__check(buttons)
        self._buttons = buttons
        super().__init__(**kwargs)

    @property
    def buttons(self) -> list[Button]:
        return self._buttons
