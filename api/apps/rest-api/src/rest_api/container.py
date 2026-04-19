from dependency_injector import containers, providers

from typeforms_domain.core.service.field_definition_domain_service import (
    FieldDefinitionDomainServiceImpl,
)
from typeforms_domain.application_service.field_definition_application_service_impl import (
    FieldDefinitionApplicationServiceImpl,
)


class Container(containers.DeclarativeContainer):
    field_definition_domain_service = providers.Factory(
        FieldDefinitionDomainServiceImpl
    )

    field_definition_application_service = providers.Factory(
        FieldDefinitionApplicationServiceImpl,
        field_definition_domain_service=field_definition_domain_service,
    )
