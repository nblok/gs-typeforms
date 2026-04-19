import typing as t
import logging

from typeforms_domain.application_service.dto.form_dtos import CreateFormCommand
from typeforms_domain.application_service.ports.input.service.form_application_serivce import FormApplicationService
from typeforms_domain.application_service.ports.output.repository.uow import AbstractUnitOfWork
from typeforms_domain.core.entity.form import Form
from typeforms_domain.core.valueobject.form_id import FormId

T = t.TypeVar("T", bound=AbstractUnitOfWork)

logger = logging.getLogger(__name__)


class FormApplicationServiceImpl(FormApplicationService):
    def __init__(self, uow: T):
        self._uow = uow

    async def create_form(self, create_form_command: CreateFormCommand) -> FormId:
        logger.info(f"Creating form: {create_form_command.model_dump()}")
        async with self._uow:
            formId = await self._uow.forms.save(
                Form.create(
                    title=create_form_command.title,
                    fields=[field.model_dump() for field in create_form_command.fields]
                )
            )
        return formId
