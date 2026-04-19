import typing as t

from typeforms_domain.core.valueobject.field_definition import (
    FIELD_DEFINITIONS,
    FieldDefinition,
    FieldType,
)


class FieldDefinitionDomainService(t.Protocol):
    def get_field_definitions(self) -> list[FieldDefinition]: ...

    def get_field_definition_by_type(
        self, field_type: FieldType
    ) -> FieldDefinition | None: ...


class FieldDefinitionDomainServiceImpl(FieldDefinitionDomainService):
    def get_field_definitions(self) -> list[FieldDefinition]:
        return FIELD_DEFINITIONS

    def get_field_definition_by_type(
        self, field_type: FieldType
    ) -> FieldDefinition | None:
        return next((fd for fd in FIELD_DEFINITIONS if fd.type == field_type), None)
