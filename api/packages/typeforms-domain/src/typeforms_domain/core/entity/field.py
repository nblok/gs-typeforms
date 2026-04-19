import uuid

from common.domain.entity.base_entity import Entity
from typeforms_domain.core.valueobject.field_definition import FieldType
from typeforms_domain.core.valueobject.field_id import FieldId


class Field(Entity[FieldId]):
    def __init__(
        self,
        field_id: FieldId,
        label: str,
        field_type: FieldType,
        order: int,
        required: bool,
    ):
        super().__init__(field_id)
        self.label = label
        self.field_type = field_type
        self.order = order
        self.required = required

    @classmethod
    def create(cls, label: str, field_type: FieldType, order: int, required: bool = False) -> "Field":
        return cls(
            field_id=FieldId(value=uuid.uuid4()),
            label=label,
            field_type=field_type,
            order=order,
            required=required,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id.value),
            "label": self.label,
            "field_type": self.field_type.value,
            "order": self.order,
            "required": self.required,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Field":
        return cls(
            field_id=FieldId(value=uuid.UUID(data["field_id"])),
            label=data["label"],
            field_type=FieldType(data["field_type"]),
            order=data["order"],
            required=data["required"],
        )