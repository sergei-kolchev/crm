from functools import cached_property


class HTMLAttributes:
    def __init__(self, attrs: dict):
        if not attrs:
            raise ValueError("'attrs' can't be an empty or None type")
        if type(attrs) is not dict:
            raise TypeError("Expected dict type for 'attrs'")
        self.__attrs = attrs

    @classmethod
    def to_raw(cls, attrs: dict) -> str:
        return " ".join([f'{k}="{v}"' for k, v in attrs.items()])

    @property
    def attrs(self) -> dict:
        return self.__attrs

    @cached_property
    def raw(self) -> str:
        return self.to_raw(self.attrs)

    def __call__(self):
        return self.raw

    def __str__(self):
        return self.attrs
