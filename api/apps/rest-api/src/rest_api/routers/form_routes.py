import logging
import typing as t
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from rest_api.container import Container
from typeforms_domain.application_service.dto.form_dtos import (
    CreateFormCommand,
    FormResponseDto,
    FormSummaryDto,
)
from typeforms_domain.application_service.ports.input.service.form_application_serivce import (
    FormApplicationService,
)
from typeforms_domain.core.valueobject.form_id import FormId

router = APIRouter(
    prefix="/forms",
    tags=["Forms"],
)

logger = logging.getLogger(__name__)


@router.get("/", response_model=list[FormSummaryDto])
@inject
async def list_forms(
    form_application_service: t.Annotated[
        FormApplicationService,
        Depends(Provide[Container.form_application_service]),
    ],
):
    return await form_application_service.list_forms()


@router.post("/")
@inject
async def create_form(
    create_form_command: CreateFormCommand,
    form_application_service: t.Annotated[
        FormApplicationService,
        Depends(Provide[Container.form_application_service]),
    ],
):
    form_id = await form_application_service.create_form(
        create_form_command=create_form_command
    )
    return {"id": str(form_id.value)}


@router.get("/{form_id}", response_model=FormResponseDto)
@inject
async def get_form(
    form_id: uuid.UUID,
    form_application_service: t.Annotated[
        FormApplicationService,
        Depends(Provide[Container.form_application_service]),
    ],
):
    form = await form_application_service.get_form(FormId(value=form_id))
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return form
