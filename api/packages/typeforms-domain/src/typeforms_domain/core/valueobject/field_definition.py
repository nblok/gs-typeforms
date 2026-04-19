import typing as t
from dataclasses import dataclass
from enum import StrEnum

from common.domain.valueobject.value_object import ValueObject


# ---------------------------------------------------------------------------
# Config shapes — each field type carries its own strongly-typed config
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ShortTextConfig:
    placeholder: str
    max_length: int | None


@dataclass(frozen=True)
class LongTextConfig:
    placeholder: str
    max_length: int | None


@dataclass(frozen=True)
class MultipleChoiceConfig:
    options: tuple[str, ...]
    allow_multiple: bool


@dataclass(frozen=True)
class YesNoConfig:
    true_label: str
    false_label: str


@dataclass(frozen=True)
class RatingConfig:
    max_value: int
    label: str


# ---------------------------------------------------------------------------
# Discriminated union — one variant per supported field type
# ---------------------------------------------------------------------------


class FieldType(StrEnum):
    SHORT_TEXT = "short_text"
    LONG_TEXT = "long_text"
    MULTIPLE_CHOICE = "multiple_choice"
    YES_NO = "yes_no"
    RATING = "rating"


FieldConfig = t.Union[
    ShortTextConfig, LongTextConfig, MultipleChoiceConfig, YesNoConfig, RatingConfig
]


# ---------------------------------------------------------------------------
# Value object
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldDefinition(ValueObject):
    type: FieldType
    label: str
    description: str
    icon: str
    default_config: FieldConfig


# ---------------------------------------------------------------------------
# Registry — the canonical list of supported field definitions
# ---------------------------------------------------------------------------

FIELD_DEFINITIONS: list[FieldDefinition] = [
    FieldDefinition(
        type=FieldType.SHORT_TEXT,
        label="Short Text",
        description="A single-line text input for brief answers",
        icon="type",
        default_config=ShortTextConfig(
            placeholder="Type your answer here...", max_length=None
        ),
    ),
    FieldDefinition(
        type=FieldType.LONG_TEXT,
        label="Long Text",
        description="A multi-line text area for detailed responses",
        icon="align-left",
        default_config=LongTextConfig(
            placeholder="Type your answer here...", max_length=None
        ),
    ),
    FieldDefinition(
        type=FieldType.MULTIPLE_CHOICE,
        label="Multiple Choice",
        description="Let respondents pick from a list of options",
        icon="list",
        default_config=MultipleChoiceConfig(
            options=("Option 1", "Option 2"), allow_multiple=False
        ),
    ),
    FieldDefinition(
        type=FieldType.YES_NO,
        label="Yes / No",
        description="A simple binary choice question",
        icon="toggle-left",
        default_config=YesNoConfig(true_label="Yes", false_label="No"),
    ),
    FieldDefinition(
        type=FieldType.RATING,
        label="Rating",
        description="Ask respondents to rate something on a numeric scale",
        icon="star",
        default_config=RatingConfig(max_value=5, label="Rating"),
    ),
]
