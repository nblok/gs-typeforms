import json

from databases import Database
from typeforms_domain.application_service.ports.output.repository.response_repository import (
    ResponseRepository,
)
from typeforms_domain.core.entity.response import Response
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.core.valueobject.respondent_id import RespondentId
from typeforms_domain.core.valueobject.response_id import ResponseId

GET_BY_RESPONDENT_SQL = """
SELECT id, form_id, respondent_id, answers, submitted_at, modified_at
FROM response
WHERE form_id = :form_id AND respondent_id = :respondent_id
"""

LIST_BY_FORM_SQL = """
SELECT id, form_id, respondent_id, answers, submitted_at, modified_at
FROM response
WHERE form_id = :form_id
ORDER BY submitted_at
"""

SAVE_UPSERT_SQL = """
INSERT INTO response (id, form_id, respondent_id, answers)
VALUES (:id, :form_id, :respondent_id, :answers)
ON CONFLICT (form_id, respondent_id) DO UPDATE SET
    answers = EXCLUDED.answers,
    modified_at = CURRENT_TIMESTAMP
"""


class DatabasesResponseRepository(ResponseRepository):
    def __init__(self, db: Database):
        self._db = db

    async def get_by_respondent(
        self,
        form_id: FormId,
        respondent_id: RespondentId,
    ) -> Response | None:
        row = await self._db.fetch_one(
            GET_BY_RESPONDENT_SQL,
            {
                "form_id": str(form_id.value),
                "respondent_id": str(respondent_id.value),
            },
        )
        if row is None:
            return None
        return Response.from_dict(
            {
                "response_id": str(row["id"]),
                "form_id": str(row["form_id"]),
                "respondent_id": str(row["respondent_id"]),
                "answers": json.loads(row["answers"]),
                "submitted_at": row["submitted_at"],
                "modified_at": row["modified_at"],
            }
        )

    async def list_by_form(self, form_id: FormId) -> list[Response]:
        rows = await self._db.fetch_all(
            LIST_BY_FORM_SQL,
            {"form_id": str(form_id.value)},
        )
        return [
            Response.from_dict(
                {
                    "response_id": str(row["id"]),
                    "form_id": str(row["form_id"]),
                    "respondent_id": str(row["respondent_id"]),
                    "answers": json.loads(row["answers"]),
                    "submitted_at": row["submitted_at"],
                    "modified_at": row["modified_at"],
                }
            )
            for row in rows
        ]

    async def save(self, response: Response) -> ResponseId:
        await self._db.execute(
            SAVE_UPSERT_SQL,
            {
                "id": str(response.id.value),
                "form_id": str(response.form_id.value),
                "respondent_id": str(response.respondent_id.value),
                "answers": json.dumps(response.answers),
            },
        )
        return response.id
