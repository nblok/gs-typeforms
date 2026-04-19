import typing as t

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from rest_api.container import Container
from typeforms_domain.application_service.dto.field_definition_dtos import (
    FieldDefinitionResponsesDto,
)
from typeforms_domain.application_service.ports.service.field_definition_service import (
    FieldDefinitionApplicationService,
)

router = APIRouter(
    prefix="/field-definitions",
    tags=["Field Definitions"],
)


@router.get("/", response_model=FieldDefinitionResponsesDto)
@inject
async def get_field_definitions(
    field_definition_application_service: t.Annotated[
        FieldDefinitionApplicationService,
        Depends(Provide[Container.field_definition_application_service]),
    ],
):
    return field_definition_application_service.get_field_definitions()
