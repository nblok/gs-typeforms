import typing as t

from typeforms_domain.application_service.dto.field_definition_dtos import (
    FieldDefinitionResponseDto,
    FieldDefinitionResponsesDto,
)
from typeforms_domain.core.valueobject.field_definition import FieldType


class FieldDefinitionApplicationService(t.Protocol):
    def get_field_definition_by_type(
        self, field_type: FieldType
    ) -> t.Optional[FieldDefinitionResponseDto]: ...

    def get_field_definitions(self) -> FieldDefinitionResponsesDto: ...
