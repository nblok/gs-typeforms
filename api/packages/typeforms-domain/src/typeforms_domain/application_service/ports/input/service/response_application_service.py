import typing as t

from typeforms_domain.application_service.dto.response_dtos import (
    ResponseDto,
    SubmitResponseCommand,
)
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.core.valueobject.respondent_id import RespondentId


class ResponseApplicationService(t.Protocol):
    async def submit_response(
        self,
        form_id: FormId,
        command: SubmitResponseCommand,
    ) -> ResponseDto:
        pass

    async def get_response_by_respondent(
        self,
        form_id: FormId,
        respondent_id: RespondentId,
    ) -> ResponseDto | None:
        pass

    async def list_responses_for_form(
        self,
        form_id: FormId,
    ) -> list[ResponseDto]:
        pass
