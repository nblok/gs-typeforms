import json

from databases import Database
from typeforms_domain.core.entity.form import Form
from typeforms_domain.core.valueobject.form_id import FormId
from typeforms_domain.application_service.ports.output.repository.form_repository import FormRepository

GET_QUERY_SQL = """
SELECT id AS form_id, title, fields, created_at, modified_at 
FROM form WHERE id = :id
"""

SAVE_INSERT_FORM_SQL = """
INSERT INTO form (id, title)
VALUES (:id, :title)
ON CONFLICT (id) DO UPDATE SET
title = EXCLUDED.title, modified_at = CURRENT_TIMESTAMP
"""

SAVE_INSERT_FIELD_SQL = """
INSERT INTO field (id, form_id, label, field_type, "order", required)
VALUES (:id, :form_id, :label, :field_type, :order, :required)
    ON CONFLICT (id) DO UPDATE SET
    label = EXCLUDED.label,
    field_type = EXCLUDED.field_type,
    "order" = EXCLUDED."order",
    required = EXCLUDED.required
"""


class DatabasesFormRepository(FormRepository):
    def __init__(self, db: Database):
        self._db = db

    async def get(self, form_id: FormId) -> Form | None:
        row = await self._db.fetch_one(
            GET_QUERY_SQL, {"id": form_id.value},
        )
        if row is None:
            return None
        data = dict(row)
        if isinstance(data["fields"], str):
            data["fields"] = json.loads(data["fields"])
        return Form.from_dict(data)

    async def save(self, form: Form) -> FormId:
        await self._db.execute(
            SAVE_INSERT_FORM_SQL,
            {
                "id": form.id.value,
                "title": form.title,
            },
        )

        if form.fields:
            await self._db.execute_many(
                SAVE_INSERT_FIELD_SQL,
                [
                    {
                        "id": str(field.id.value),
                        "form_id": str(form.id.value),
                        "label": field.label,
                        "field_type": field.field_type.value,
                        "order": field.order,
                        "required": field.required,
                    }
                    for field in form.fields
                ],
            )

        return form.id
