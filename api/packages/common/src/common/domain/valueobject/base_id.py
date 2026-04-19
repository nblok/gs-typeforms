import typing as t
from dataclasses import dataclass

from common.domain.valueobject.value_object import ValueObject

T = t.TypeVar("T")


@dataclass(frozen=True)
class BaseId(ValueObject, t.Generic[T]):
    value: T
