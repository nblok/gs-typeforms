import dataclasses
import uuid

from common.domain.entity.base_entity import Entity
from typeforms_domain.core.valueobject.field_definition import (
    FieldConfig,
    FieldType,
    field_config_for,
)
from typeforms_domain.core.valueobject.field_id import FieldId


class Field(Entity[FieldId]):
    def __init__(
        self,
        field_id: FieldId,
        label: str,
        field_type: FieldType,
        order: int,
        required: bool,
        config: FieldConfig,
    ):
        if config.TYPE is not field_type:
            raise ValueError(
                f"Config type {config.TYPE} does not match field_type {field_type}"
            )
        super().__init__(field_id)
        self.label = label
        self.field_type = field_type
        self.order = order
        self.required = required
        self.config = config

    @classmethod
    def create(
        cls,
        label: str,
        field_type: FieldType,
        order: int,
        config: FieldConfig,
        required: bool = False,
    ) -> "Field":
        return cls(
            field_id=FieldId(value=uuid.uuid4()),
            label=label,
            field_type=field_type,
            order=order,
            required=required,
            config=config,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id.value),
            "label": self.label,
            "field_type": self.field_type.value,
            "order": self.order,
            "required": self.required,
            "config": dataclasses.asdict(self.config),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Field":
        field_type = FieldType(data["field_type"])
        return cls(
            field_id=FieldId(value=uuid.UUID(data["field_id"])),
            label=data["label"],
            field_type=field_type,
            order=data["order"],
            required=data["required"],
            config=field_config_for(field_type, data["config"]),
        )
