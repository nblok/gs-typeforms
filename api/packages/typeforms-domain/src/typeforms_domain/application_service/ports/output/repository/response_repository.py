import typing as t

from typeforms_domain.core.entity.response import Response
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.core.valueobject.respondent_id import RespondentId
from typeforms_domain.core.valueobject.response_id import ResponseId


class ResponseRepository(t.Protocol):
    async def get_by_respondent(
        self,
        form_id: FormId,
        respondent_id: RespondentId,
    ) -> Response | None: ...

    async def save(self, response: Response) -> ResponseId: ...
