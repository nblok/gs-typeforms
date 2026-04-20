import datetime

from pydantic import BaseModel

from typeforms_domain.application_service.dto.field_definition_dtos import (
    FieldConfigDto,
)
from typeforms_domain.core.valueobject.field_definition import FieldType


class CreateFormField(BaseModel):
    label: str
    field_type: FieldType
    order: int
    required: bool
    config: FieldConfigDto


class CreateFormCommand(BaseModel):
    title: str
    fields: list[CreateFormField]


class FieldResponseDto(BaseModel):
    id: str
    label: str
    field_type: FieldType
    order: int
    required: bool
    config: FieldConfigDto


class FormResponseDto(BaseModel):
    id: str
    title: str
    fields: list[FieldResponseDto]
    created_at: datetime.datetime | None
    modified_at: datetime.datetime | None
