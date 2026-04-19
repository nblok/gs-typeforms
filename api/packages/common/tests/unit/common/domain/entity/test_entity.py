from common.domain.entity.base_entity import Entity
from common.domain.entity.aggregate_root import AggregateRoot


class ConcreteEntity(Entity[int]):
    pass


class AnotherEntity(Entity[int]):
    pass


class TestEntityEquality:
    def test_equal_when_same_id(self):
        assert ConcreteEntity(1) == ConcreteEntity(1)

    def test_not_equal_when_different_id(self):
        assert ConcreteEntity(1) != ConcreteEntity(2)

    def test_not_equal_when_different_type_same_id(self):
        assert ConcreteEntity(1) != AnotherEntity(1)

    def test_not_equal_to_non_entity(self):
        assert ConcreteEntity(1) != 1

    def test_same_instance_is_equal(self):
        entity = ConcreteEntity(1)
        assert entity == entity


class TestEntityHash:
    def test_same_id_same_hash(self):
        assert hash(ConcreteEntity(1)) == hash(ConcreteEntity(1))

    def test_different_id_different_hash(self):
        assert hash(ConcreteEntity(1)) != hash(ConcreteEntity(2))

    def test_usable_in_set(self):
        entities = {ConcreteEntity(1), ConcreteEntity(1), ConcreteEntity(2)}
        assert len(entities) == 2

    def test_usable_as_dict_key(self):
        d = {ConcreteEntity(1): "a", ConcreteEntity(2): "b"}
        assert d[ConcreteEntity(1)] == "a"


class TestEntityId:
    def test_id_property_returns_value(self):
        assert ConcreteEntity(42).id == 42

    def test_id_with_string(self):
        class StringEntity(Entity[str]):
            pass

        assert StringEntity("abc").id == "abc"


class TestAggregateRoot:
    def test_is_entity_subclass(self):
        assert issubclass(AggregateRoot, Entity)

    def test_equality_inherited(self):
        class OrderId(AggregateRoot[int]):
            pass

        assert OrderId(1) == OrderId(1)
        assert OrderId(1) != OrderId(2)

    def test_hash_inherited(self):
        class OrderId(AggregateRoot[int]):
            pass

        assert hash(OrderId(1)) == hash(OrderId(1))
        assert {OrderId(1), OrderId(1)} == {OrderId(1)}
