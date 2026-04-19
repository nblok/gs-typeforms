from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))
