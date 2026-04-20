import typing as t

from typeforms_domain.application_service.dto.form_dtos import (
    CreateFormCommand,
    FormResponseDto,
)
from typeforms_domain.core.valueobject.form_id import FormId


class FormApplicationService(t.Protocol):

    async def create_form(self, create_form_command: CreateFormCommand) -> FormId:
        pass

    async def get_form(self, form_id: FormId) -> FormResponseDto | None:
        pass
