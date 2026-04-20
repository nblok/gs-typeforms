import dataclasses
import logging
import typing as t

from typeforms_domain.application_service.dto.field_definition_dtos import (
    FieldConfigDto,
    LongTextConfigDto,
    MultipleChoiceConfigDto,
    RatingConfigDto,
    ShortTextConfigDto,
    YesNoConfigDto,
)
from typeforms_domain.application_service.dto.form_dtos import (
    CreateFormCommand,
    CreateFormField,
    FieldResponseDto,
    FormResponseDto,
    FormSummaryDto,
)
from typeforms_domain.application_service.ports.input.service.form_application_serivce import (
    FormApplicationService,
)
from typeforms_domain.application_service.ports.output.repository.uow import (
    AbstractUnitOfWork,
)
from typeforms_domain.core.entity.field import Field
from typeforms_domain.core.entity.form import Form
from typeforms_domain.core.valueobject.field_definition import (
    FieldConfig,
    FieldType,
    field_config_for,
)
from typeforms_domain.core.valueobject.form_id import FormId

T = t.TypeVar("T", bound=AbstractUnitOfWork)

logger = logging.getLogger(__name__)


_CONFIG_DTO_BY_TYPE: dict[FieldType, type] = {
    FieldType.SHORT_TEXT: ShortTextConfigDto,
    FieldType.LONG_TEXT: LongTextConfigDto,
    FieldType.MULTIPLE_CHOICE: MultipleChoiceConfigDto,
    FieldType.YES_NO: YesNoConfigDto,
    FieldType.RATING: RatingConfigDto,
}


def _dto_to_field_config(dto: FieldConfigDto) -> FieldConfig:
    data = dto.model_dump()
    return field_config_for(data["type"], data)


def _config_to_dto(config: FieldConfig) -> FieldConfigDto:
    data = dataclasses.asdict(config)
    data["type"] = config.TYPE
    dto_cls = _CONFIG_DTO_BY_TYPE[config.TYPE]
    return dto_cls(**data)


def _dto_to_field(dto: CreateFormField) -> Field:
    return Field.create(
        label=dto.label,
        field_type=dto.field_type,
        order=dto.order,
        required=dto.required,
        config=_dto_to_field_config(dto.config),
    )


def _field_to_response_dto(field: Field) -> FieldResponseDto:
    return FieldResponseDto(
        id=str(field.id.value),
        label=field.label,
        field_type=field.field_type,
        order=field.order,
        required=field.required,
        config=_config_to_dto(field.config),
    )


def _form_to_response_dto(form: Form) -> FormResponseDto:
    return FormResponseDto(
        id=str(form.id.value),
        title=form.title,
        fields=[_field_to_response_dto(f) for f in form.fields],
        created_at=form.created_at,
        modified_at=form.modified_at,
    )


class FormApplicationServiceImpl(FormApplicationService):
    def __init__(self, uow: T):
        self._uow = uow

    async def create_form(self, create_form_command: CreateFormCommand) -> FormId:
        logger.info(f"Creating form: {create_form_command.model_dump()}")
        fields = [_dto_to_field(f) for f in create_form_command.fields]
        form = Form.create(title=create_form_command.title, fields=fields)
        async with self._uow:
            form_id = await self._uow.forms.save(form)
        return form_id

    async def get_form(self, form_id: FormId) -> FormResponseDto | None:
        logger.info(f"Getting form: {form_id.value}")
        async with self._uow:
            form = await self._uow.forms.get(form_id)
        if form is None:
            return None
        return _form_to_response_dto(form)

    async def list_forms(self) -> list[FormSummaryDto]:
        logger.info("Listing all forms")
        async with self._uow:
            forms = await self._uow.forms.find_all()
        return [
            FormSummaryDto(id=str(f.id.value), title=f.title, created_at=f.created_at)
            for f in forms
        ]
