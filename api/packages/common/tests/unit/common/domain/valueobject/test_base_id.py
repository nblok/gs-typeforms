from uuid import UUID

from common.domain.valueobject.base_id import BaseId


class IntId(BaseId[int]):
    pass


class OtherId(BaseId[int]):
    pass


class UuidId(BaseId[UUID]):
    pass


class TestBaseIdEquality:
    def test_equal_when_same_value(self):
        assert IntId(1) == IntId(1)

    def test_not_equal_when_different_value(self):
        assert IntId(1) != IntId(2)

    def test_not_equal_when_different_subclass_same_value(self):
        assert IntId(1) != OtherId(1)

    def test_not_equal_to_raw_value(self):
        assert IntId(1) != 1

    def test_same_instance_is_equal(self):
        id_ = IntId(1)
        assert id_ == id_


class TestBaseIdHash:
    def test_same_value_same_hash(self):
        assert hash(IntId(1)) == hash(IntId(1))

    def test_different_value_different_hash(self):
        assert hash(IntId(1)) != hash(IntId(2))

    def test_usable_in_set(self):
        ids = {IntId(1), IntId(1), IntId(2)}
        assert len(ids) == 2

    def test_usable_as_dict_key(self):
        d = {IntId(1): "a", IntId(2): "b"}
        assert d[IntId(1)] == "a"


class TestBaseIdValue:
    def test_value_property_returns_int(self):
        assert IntId(42).value == 42

    def test_value_property_returns_uuid(self):
        uid = UUID("12345678-1234-5678-1234-567812345678")
        assert UuidId(uid).value == uid
