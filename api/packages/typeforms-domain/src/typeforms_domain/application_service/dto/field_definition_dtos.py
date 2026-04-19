import typing as t
from pydantic import BaseModel, Field

from typeforms_domain.core.valueobject.field_definition import FieldType


class ShortTextConfigDto(BaseModel):
    type: t.Literal[FieldType.SHORT_TEXT] = FieldType.SHORT_TEXT
    placeholder: str
    max_length: int | None


class LongTextConfigDto(BaseModel):
    type: t.Literal[FieldType.LONG_TEXT] = FieldType.LONG_TEXT
    placeholder: str
    max_length: int | None


class MultipleChoiceConfigDto(BaseModel):
    type: t.Literal[FieldType.MULTIPLE_CHOICE] = FieldType.MULTIPLE_CHOICE
    options: list[str]
    allow_multiple: bool


class YesNoConfigDto(BaseModel):
    type: t.Literal[FieldType.YES_NO] = FieldType.YES_NO
    true_label: str
    false_label: str


class RatingConfigDto(BaseModel):
    type: t.Literal[FieldType.RATING] = FieldType.RATING
    max_value: int
    label: str


FieldConfigDto = t.Annotated[
    t.Union[
        ShortTextConfigDto,
        LongTextConfigDto,
        MultipleChoiceConfigDto,
        YesNoConfigDto,
        RatingConfigDto,
    ],
    Field(discriminator="type"),
]


class FieldDefinitionResponseDto(BaseModel):
    type: FieldType
    label: str
    description: str
    icon: str
    default_config: FieldConfigDto


FieldDefinitionResponsesDto: t.TypeAlias = list[FieldDefinitionResponseDto]
