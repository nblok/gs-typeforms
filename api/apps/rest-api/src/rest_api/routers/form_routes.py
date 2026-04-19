import typing as t
import logging

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from rest_api.container import Container
from typeforms_domain.application_service.dto.form_dtos import CreateFormCommand
from typeforms_domain.application_service.ports.input.service.form_application_serivce import FormApplicationService

router = APIRouter(
    prefix="/forms",
    tags=["Forms"],
)

logger = logging.getLogger(__name__)

@router.post("/")
@inject
async def create_form(
    create_form_command: CreateFormCommand,
    form_application_service: t.Annotated[
        FormApplicationService,
        Depends(Provide[Container.form_application_service]),
    ],
):
    form_id = await form_application_service.create_form(create_form_command=create_form_command)
    return {"id": str(form_id.value)}
