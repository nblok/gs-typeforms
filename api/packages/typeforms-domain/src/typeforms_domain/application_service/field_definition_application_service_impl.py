import typing as t
import dataclasses
from typeforms_domain.application_service.dto.field_definition_dtos import (
    FieldDefinitionResponseDto,
    FieldDefinitionResponsesDto,
)

from typeforms_domain.application_service.ports.service.field_definition_service import (
    FieldDefinitionApplicationService,
)
from typeforms_domain.core.service.field_definition_domain_service import (
    FieldDefinitionDomainService,
)
from typeforms_domain.core.valueobject.field_definition import FieldType


class FieldDefinitionApplicationServiceImpl(FieldDefinitionApplicationService):
    def __init__(self, field_definition_domain_service: FieldDefinitionDomainService):
        self._field_definition_domain_service = field_definition_domain_service

    @staticmethod
    def _to_response_dto(field_def) -> FieldDefinitionResponseDto:
        d = dataclasses.asdict(field_def)
        d["default_config"]["type"] = field_def.type
        return FieldDefinitionResponseDto(**d)

    def get_field_definitions(self) -> FieldDefinitionResponsesDto:
        return list(
            map(
                self._to_response_dto,
                self._field_definition_domain_service.get_field_definitions(),
            )
        )

    def get_field_definition_by_type(
        self, field_type: FieldType
    ) -> t.Optional[FieldDefinitionResponseDto]:
        result = None
        if (field_definition := self._field_definition_domain_service.get_field_definition_by_type(
            field_type
        )):
            result = self._to_response_dto(field_definition)
        return result

