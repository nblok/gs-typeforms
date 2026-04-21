import datetime
import typing as t
import uuid

from common.domain.entity.aggregate_root import AggregateRoot
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.core.valueobject.respondent_id import RespondentId
from typeforms_domain.core.valueobject.response_id import ResponseId


class Response(AggregateRoot[ResponseId]):
    def __init__(
        self,
        response_id: ResponseId,
        form_id: FormId,
        respondent_id: RespondentId,
        answers: dict[str, t.Any],
        submitted_at: datetime.datetime | None = None,
        modified_at: datetime.datetime | None = None,
    ):
        super().__init__(response_id)
        self.form_id = form_id
        self.respondent_id = respondent_id
        self.answers = answers
        self.submitted_at = submitted_at
        self.modified_at = modified_at

    @classmethod
    def create(
        cls,
        form_id: FormId,
        respondent_id: RespondentId,
        answers: dict[str, t.Any],
    ) -> "Response":
        return cls(
            response_id=ResponseId(value=uuid.uuid4()),
            form_id=form_id,
            respondent_id=respondent_id,
            answers=answers,
        )

    def update_answers(self, answers: dict[str, t.Any]) -> None:
        self.answers = answers

    @classmethod
    def from_dict(cls, data: dict) -> "Response":
        return cls(
            response_id=ResponseId(value=uuid.UUID(data["response_id"])),
            form_id=FormId(value=uuid.UUID(data["form_id"])),
            respondent_id=RespondentId(value=uuid.UUID(data["respondent_id"])),
            answers=data["answers"],
            submitted_at=data.get("submitted_at"),
            modified_at=data.get("modified_at"),
        )
