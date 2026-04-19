from pydantic import BaseModel

from typeforms_domain.core.valueobject.field_definition import FieldType


class CreateFormField(BaseModel):
    label: str
    field_type: FieldType
    order: int
    required: bool


class CreateFormCommand(BaseModel):
    title: str
    fields: list[CreateFormField]