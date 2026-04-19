import typing as t

TId = t.TypeVar("TId")


class Entity(t.Generic[TId]):
    def __init__(self, id: TId) -> None:
        self._id = id

    @property
    def id(self) -> TId:
        return self._id

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        # TODO: remove assert? I would think that throwing exception
        #       may make more sense in production code
        assert isinstance(other, Entity)
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)
