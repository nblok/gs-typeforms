import logging
import typing as t
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from rest_api.container import Container
from typeforms_domain.application_service.dto.response_dtos import (
    ResponseDto,
    SubmitResponseCommand,
)
from typeforms_domain.application_service.ports.input.service.response_application_service import (
    ResponseApplicationService,
)
from typeforms_domain.application_service.response_application_service_impl import (
    FormNotFoundError,
)
from typeforms_domain.core.valueobject.field_definition import (
    FieldConfigValidationError,
)
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.core.valueobject.respondent_id import RespondentId

router = APIRouter(
    prefix="/forms/{form_id}/responses",
    tags=["Responses"],
)

logger = logging.getLogger(__name__)


@router.get("", response_model=list[ResponseDto])
@inject
async def list_responses(
    form_id: uuid.UUID,
    response_application_service: t.Annotated[
        ResponseApplicationService,
        Depends(Provide[Container.response_application_service]),
    ],
):
    try:
        return await response_application_service.list_responses_for_form(
            form_id=FormId(value=form_id),
        )
    except FormNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("", response_model=ResponseDto)
@inject
async def submit_response(
    form_id: uuid.UUID,
    command: SubmitResponseCommand,
    response_application_service: t.Annotated[
        ResponseApplicationService,
        Depends(Provide[Container.response_application_service]),
    ],
):
    try:
        return await response_application_service.submit_response(
            form_id=FormId(value=form_id),
            command=command,
        )
    except FormNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except FieldConfigValidationError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/respondents/{respondent_id}", response_model=ResponseDto | None)
@inject
async def get_response_by_respondent(
    form_id: uuid.UUID,
    respondent_id: uuid.UUID,
    response_application_service: t.Annotated[
        ResponseApplicationService,
        Depends(Provide[Container.response_application_service]),
    ],
):
    return await response_application_service.get_response_by_respondent(
        form_id=FormId(value=form_id),
        respondent_id=RespondentId(value=respondent_id),
    )
