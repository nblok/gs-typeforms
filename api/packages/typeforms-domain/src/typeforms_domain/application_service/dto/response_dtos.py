import datetime
import typing as t

from pydantic import BaseModel


class SubmitResponseCommand(BaseModel):
    respondent_id: str
    answers: dict[str, t.Any]


class ResponseDto(BaseModel):
    id: str
    form_id: str
    respondent_id: str
    answers: dict[str, t.Any]
    submitted_at: datetime.datetime | None
    modified_at: datetime.datetime | None
