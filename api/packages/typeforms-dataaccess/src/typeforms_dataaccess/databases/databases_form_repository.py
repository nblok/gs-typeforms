import json

from databases import Database
from typeforms_domain.application_service.ports.output.repository.form_repository import (
    FormRepository,
)
from typeforms_domain.core.entity.form import Form
from typeforms_domain.core.valueobject.form_id import FormId

GET_FORM_SQL = """
SELECT id, title, created_at, modified_at
FROM form WHERE id = :id
"""

GET_ALL_FORMS_SQL = """
                    SELECT id, title, created_at, modified_at
                    FROM form
                    ORDER BY created_at DESC \
                    """

GET_FIELDS_SQL = """
                 SELECT id, form_id, label, field_type, "order", required, config
                 FROM field
                 WHERE form_id = :form_id
                 ORDER BY "order" \
                 """

GET_ALL_FIELDS_SQL = """
                     SELECT id, form_id, label, field_type, "order", required, config
                     FROM field
                     ORDER BY form_id, "order" \
                     """

SAVE_INSERT_FORM_SQL = """
INSERT INTO form (id, title)
VALUES (:id, :title)
ON CONFLICT (id) DO UPDATE SET
title = EXCLUDED.title, modified_at = CURRENT_TIMESTAMP
"""

SAVE_INSERT_FIELD_SQL = """
INSERT INTO field (id, form_id, label, field_type, "order", required, config)
VALUES (:id, :form_id, :label, :field_type, :order, :required, :config)
    ON CONFLICT (id) DO UPDATE SET
    label = EXCLUDED.label,
    field_type = EXCLUDED.field_type,
    "order" = EXCLUDED."order",
    required = EXCLUDED.required,
    config = EXCLUDED.config
"""


class DatabasesFormRepository(FormRepository):
    def __init__(self, db: Database):
        self._db = db

    async def get(self, form_id: FormId) -> Form | None:
        form_row = await self._db.fetch_one(GET_FORM_SQL, {"id": str(form_id.value)})
        if form_row is None:
            return None
        field_rows = await self._db.fetch_all(
            GET_FIELDS_SQL, {"form_id": str(form_id.value)}
        )
        data = {
            "form_id": str(form_row["id"]),
            "title": form_row["title"],
            "created_at": form_row["created_at"],
            "modified_at": form_row["modified_at"],
            "fields": [
                {
                    "field_id": str(row["id"]),
                    "label": row["label"],
                    "field_type": row["field_type"],
                    "order": row["order"],
                    "required": bool(row["required"]),
                    "config": json.loads(row["config"]),
                }
                for row in field_rows
            ],
        }
        return Form.from_dict(data)

    async def find_all(self) -> list[Form]:
        form_rows = await self._db.fetch_all(GET_ALL_FORMS_SQL)
        if not form_rows:
            return []

        field_rows = await self._db.fetch_all(GET_ALL_FIELDS_SQL)

        # Group fields by form_id
        fields_by_form_id = {}
        for row in field_rows:
            form_id = str(row["form_id"])
            if form_id not in fields_by_form_id:
                fields_by_form_id[form_id] = []
            fields_by_form_id[form_id].append(
                {
                    "field_id": str(row["id"]),
                    "label": row["label"],
                    "field_type": row["field_type"],
                    "order": row["order"],
                    "required": bool(row["required"]),
                    "config": json.loads(row["config"]),
                }
            )

        forms = []
        for form_row in form_rows:
            form_id = str(form_row["id"])
            data = {
                "form_id": form_id,
                "title": form_row["title"],
                "created_at": form_row["created_at"],
                "modified_at": form_row["modified_at"],
                "fields": fields_by_form_id.get(form_id, []),
            }
            forms.append(Form.from_dict(data))

        return forms

    async def save(self, form: Form) -> FormId:
        await self._db.execute(
            SAVE_INSERT_FORM_SQL,
            {
                "id": str(form.id.value),
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
                        "config": json.dumps(field.to_dict()["config"]),
                    }
                    for field in form.fields
                ],
            )

        return form.id
