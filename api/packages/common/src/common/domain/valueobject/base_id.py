from typing import Generic, TypeVar

from common.domain.valueobject.value_object import ValueObject

T = TypeVar("T")


class BaseId(ValueObject, Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, BaseId)
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
