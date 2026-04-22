import datetime
import uuid

from common.domain.entity.aggregate_root import AggregateRoot
from typeforms_domain.core.entity.field import Field
from typeforms_domain.core.exception.typeforms_domain_exceptions import (
    FormValidationError,
)
from typeforms_domain.core.valueobject.form_id import FormId


class Form(AggregateRoot[FormId]):
    def __init__(
        self,
        form_id: FormId,
        title: str,
        fields: list[Field],
        created_at: datetime.datetime | None = None,
        modified_at: datetime.datetime | None = None,
    ):
        super().__init__(form_id)
        self.title = title
        self.fields = fields
        self.created_at = created_at
        self.modified_at = modified_at
        if not self.fields:
            raise FormValidationError("A form must have at least one field.")

    @classmethod
    def create(cls, title: str, fields: list[Field]) -> "Form":
        return cls(
            form_id=FormId(value=uuid.uuid4()),
            title=title,
            fields=fields or [],
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Form":
        return cls(
            form_id=FormId(value=uuid.UUID(data["form_id"])),
            title=data["title"],
            fields=[Field.from_dict(f) for f in data.get("fields", [])],
            created_at=data.get("created_at"),
            modified_at=data.get("modified_at"),
        )
