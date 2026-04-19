import typing as t

from common.domain.valueobject.value_object import ValueObject

T = t.TypeVar("T")


class BaseId(ValueObject, t.Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    @t.override
    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, BaseId)
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
