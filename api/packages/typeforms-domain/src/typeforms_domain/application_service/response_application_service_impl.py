import logging
import typing as t
import uuid

from typeforms_domain.application_service.dto.response_dtos import (
    ResponseDto,
    SubmitResponseCommand,
)
from typeforms_domain.application_service.ports.input.service.response_application_service import (
    ResponseApplicationService,
)
from typeforms_domain.application_service.ports.output.repository.uow import (
    AbstractUnitOfWork,
)
from typeforms_domain.core.entity.response import Response
from typeforms_domain.core.valueobject.field_definition import (
    FieldConfigValidationError,
)
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.core.valueobject.respondent_id import RespondentId

T = t.TypeVar("T", bound=AbstractUnitOfWork)

logger = logging.getLogger(__name__)


class ResponseNotFoundError(Exception):
    pass


class FormNotFoundError(Exception):
    pass


def _response_to_dto(response: Response) -> ResponseDto:
    return ResponseDto(
        id=str(response.id.value),
        form_id=str(response.form_id.value),
        respondent_id=str(response.respondent_id.value),
        answers=response.answers,
        submitted_at=response.submitted_at,
        modified_at=response.modified_at,
    )


class ResponseApplicationServiceImpl(ResponseApplicationService):
    def __init__(self, uow: T):
        self._uow = uow

    async def submit_response(
        self,
        form_id: FormId,
        command: SubmitResponseCommand,
    ) -> ResponseDto:
        logger.info(
            f"Submitting response for form {form_id.value}: {command.model_dump()}"
        )
        respondent_id = RespondentId(value=uuid.UUID(command.respondent_id))

        async with self._uow:
            form = await self._uow.forms.get(form_id)
            if form is None:
                raise FormNotFoundError(f"Form {form_id.value} not found")

            self._validate_answers(form.fields, command.answers)

            existing = await self._uow.responses.get_by_respondent(
                form_id, respondent_id
            )
            if existing is None:
                response = Response.create(
                    form_id=form_id,
                    respondent_id=respondent_id,
                    answers=command.answers,
                )
            else:
                existing.update_answers(command.answers)
                response = existing

            await self._uow.responses.save(response)
            saved = await self._uow.responses.get_by_respondent(
                form_id, respondent_id
            )
        assert saved is not None
        return _response_to_dto(saved)

    async def list_responses_for_form(
        self,
        form_id: FormId,
    ) -> list[ResponseDto]:
        logger.info(f"Listing responses for form {form_id.value}")
        async with self._uow:
            form = await self._uow.forms.get(form_id)
            if form is None:
                raise FormNotFoundError(f"Form {form_id.value} not found")
            responses = await self._uow.responses.list_by_form(form_id)
        return [_response_to_dto(r) for r in responses]

    async def get_response_by_respondent(
        self,
        form_id: FormId,
        respondent_id: RespondentId,
    ) -> ResponseDto | None:
        logger.info(
            f"Getting response for form {form_id.value} "
            f"by respondent {respondent_id.value}"
        )
        async with self._uow:
            response = await self._uow.responses.get_by_respondent(
                form_id, respondent_id
            )
        if response is None:
            return None
        return _response_to_dto(response)

    @staticmethod
    def _validate_answers(fields, answers: dict[str, t.Any]) -> None:
        fields_by_id = {str(f.id.value): f for f in fields}
        for field_id, answer in answers.items():
            field = fields_by_id.get(field_id)
            if field is None:
                raise FieldConfigValidationError(
                    f"Unknown field id: {field_id}"
                )
            field.config.validate(answer)
