import uuid

import pytest

from typeforms_domain.core.entity.field import Field
from typeforms_domain.core.entity.form import Form
from typeforms_domain.core.exception.typeforms_domain_exceptions import (
    FormValidationError,
)
from typeforms_domain.core.valueobject.field_definition import (
    FieldType,
    ShortTextConfig,
)
from typeforms_domain.core.valueobject.field_id import FieldId
from typeforms_domain.core.valueobject.form_id import FormId


def _make_field() -> Field:
    return Field(
        field_id=FieldId(value=uuid.uuid4()),
        label="Name",
        field_type=FieldType.SHORT_TEXT,
        order=1,
        required=False,
        config=ShortTextConfig(placeholder="", max_length=None),
    )


class TestFormInvariant:
    def test_create_with_one_field_succeeds(self):
        form = Form.create(title="My Form", fields=[_make_field()])
        assert len(form.fields) == 1

    def test_create_with_multiple_fields_succeeds(self):
        form = Form.create(title="My Form", fields=[_make_field(), _make_field()])
        assert len(form.fields) == 2

    def test_create_with_empty_fields_raises(self):
        with pytest.raises(FormValidationError):
            Form.create(title="Empty Form", fields=[])

    def test_from_dict_with_no_fields_raises(self):
        data = {
            "form_id": str(uuid.uuid4()),
            "title": "Empty Form",
            "fields": [],
        }
        with pytest.raises(FormValidationError):
            Form.from_dict(data)

    def test_init_with_no_fields_raises(self):
        with pytest.raises(FormValidationError):
            Form(
                form_id=FormId(value=uuid.uuid4()),
                title="Empty Form",
                fields=[],
            )
