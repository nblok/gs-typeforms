from dependency_injector import containers, providers

from typeforms_dataaccess.databases.database import create_database
from typeforms_dataaccess.databases.databases_unit_of_work import DatabasesUnitOfWork
from typeforms_domain.application_service.form_application_service_impl import (
    FormApplicationServiceImpl,
)
from typeforms_domain.application_service.response_application_service_impl import (
    ResponseApplicationServiceImpl,
)
from typeforms_domain.core.service.field_definition_domain_service import (
    FieldDefinitionDomainServiceImpl,
)
from typeforms_domain.application_service.field_definition_application_service_impl import (
    FieldDefinitionApplicationServiceImpl,
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(
        create_database,
        config.database_url,
    )

    unit_of_work = providers.Factory(DatabasesUnitOfWork, db=db)

    field_definition_domain_service = providers.Factory(
        FieldDefinitionDomainServiceImpl
    )

    field_definition_application_service = providers.Factory(
        FieldDefinitionApplicationServiceImpl,
        field_definition_domain_service=field_definition_domain_service,
    )

    form_application_service = providers.Factory(
        FormApplicationServiceImpl,
        uow=unit_of_work,
    )

    response_application_service = providers.Factory(
        ResponseApplicationServiceImpl,
        uow=unit_of_work,
    )
