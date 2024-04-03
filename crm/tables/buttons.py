from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import Optional


class Button(ABC):
    template_name = "tables/button.html"

    @property
    @abstractmethod
    def pk(self):
        pass

    @pk.setter
    @abstractmethod
    def pk(self, value):
        pass

    @property
    @abstractmethod
    def url(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def view_name(self):
        pass

    @abstractmethod
    def clone(self, pk: int) -> Button:
        pass


class BaseButton(Button):
    def __init__(
        self,
        name: str,
        pk: Optional[int] = None,
        url: Optional[str] = None,
        template_name: Optional[str] = None,
        view_name: Optional[str] = None,
    ) -> None:
        self.__name = name
        self.__pk = pk
        self.__view_name = view_name
        if template_name:
            self.__template_name = template_name
        if url:
            self.__url = url

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, value):
        self.__pk = value

    @property
    def url(self):
        return self.__url

    @property
    def name(self):
        return self.__name

    @property
    def view_name(self):
        return self.__view_name

    def clone(self, pk: int) -> Button:
        button = copy.deepcopy(self)
        button.pk = pk
        return button


class ConfirmButton(BaseButton):
    pass


class UpdateButton(BaseButton):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["name"] = name or "update"
        super().__init__(**kwargs)


class UpdateInlineButton(UpdateButton):
    template_name = "tables/inline_button.html"


class LeaveButton(BaseButton):
    def __init__(self, name: str = "", **kwargs) -> None:
        kwargs["name"] = name or "leave"
        super().__init__(**kwargs)


class DeleteButton(ConfirmButton):
    template_name = "tables/button_with_confirm.html"
    confirm_message = "Вы точно хотите удалить?"

    def __init__(
        self, name: str, confirm_message: Optional[str] = None, **kwargs
    ) -> None:
        kwargs["name"] = name or "delete"
        super().__init__(**kwargs)
        if confirm_message:
            self.confirm_message = confirm_message
