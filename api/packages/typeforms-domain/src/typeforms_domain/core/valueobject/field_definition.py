import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum

from common.domain.valueobject.value_object import ValueObject


class FieldConfigValidationError(ValueError):
    """Raised when a response answer violates a field's config constraints."""


class FieldType(StrEnum):
    SHORT_TEXT = "short_text"
    LONG_TEXT = "long_text"
    MULTIPLE_CHOICE = "multiple_choice"
    YES_NO = "yes_no"
    RATING = "rating"


# ---------------------------------------------------------------------------
# Config shapes — each field type carries its own strongly-typed config.
# Each config knows how to validate an answer submitted against a field of
# that type.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldConfig(ValueObject, ABC):
    TYPE: t.ClassVar[FieldType]

    @abstractmethod
    def validate(self, answer: t.Any) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class ShortTextConfig(FieldConfig):
    TYPE: t.ClassVar[FieldType] = FieldType.SHORT_TEXT
    placeholder: str
    max_length: int | None

    def validate(self, answer: t.Any) -> None:
        if not isinstance(answer, str):
            raise FieldConfigValidationError("Answer must be a string")
        if self.max_length is not None and len(answer) > self.max_length:
            raise FieldConfigValidationError(
                f"Answer exceeds max length of {self.max_length}"
            )


@dataclass(frozen=True)
class LongTextConfig(FieldConfig):
    TYPE: t.ClassVar[FieldType] = FieldType.LONG_TEXT
    placeholder: str
    max_length: int | None

    def validate(self, answer: t.Any) -> None:
        if not isinstance(answer, str):
            raise FieldConfigValidationError("Answer must be a string")
        if self.max_length is not None and len(answer) > self.max_length:
            raise FieldConfigValidationError(
                f"Answer exceeds max length of {self.max_length}"
            )


@dataclass(frozen=True)
class MultipleChoiceConfig(FieldConfig):
    TYPE: t.ClassVar[FieldType] = FieldType.MULTIPLE_CHOICE
    options: tuple[str, ...]
    allow_multiple: bool

    def validate(self, answer: t.Any) -> None:
        if self.allow_multiple:
            if not isinstance(answer, list) or not all(
                isinstance(a, str) for a in answer
            ):
                raise FieldConfigValidationError(
                    "Answer must be a list of option strings"
                )
            for choice in answer:
                if choice not in self.options:
                    raise FieldConfigValidationError(
                        f"'{choice}' is not a valid option"
                    )
        else:
            if not isinstance(answer, str):
                raise FieldConfigValidationError("Answer must be a string")
            if answer not in self.options:
                raise FieldConfigValidationError(f"'{answer}' is not a valid option")


@dataclass(frozen=True)
class YesNoConfig(FieldConfig):
    TYPE: t.ClassVar[FieldType] = FieldType.YES_NO
    true_label: str
    false_label: str

    def validate(self, answer: t.Any) -> None:
        if not isinstance(answer, bool):
            raise FieldConfigValidationError("Answer must be a boolean")


@dataclass(frozen=True)
class RatingConfig(FieldConfig):
    TYPE: t.ClassVar[FieldType] = FieldType.RATING
    max_value: int
    label: str

    def validate(self, answer: t.Any) -> None:
        if not isinstance(answer, int) or isinstance(answer, bool):
            raise FieldConfigValidationError("Answer must be an integer")
        if answer < 1 or answer > self.max_value:
            raise FieldConfigValidationError(
                f"Answer must be between 1 and {self.max_value}"
            )


_CONFIG_BY_TYPE: dict[FieldType, type[FieldConfig]] = {
    FieldType.SHORT_TEXT: ShortTextConfig,
    FieldType.LONG_TEXT: LongTextConfig,
    FieldType.MULTIPLE_CHOICE: MultipleChoiceConfig,
    FieldType.YES_NO: YesNoConfig,
    FieldType.RATING: RatingConfig,
}


def field_config_for(field_type: FieldType, data: dict) -> FieldConfig:
    """Build a FieldConfig instance from a raw dict keyed by its field type."""
    config_cls = _CONFIG_BY_TYPE[field_type]
    kwargs = {k: v for k, v in data.items() if k != "type"}
    if field_type is FieldType.MULTIPLE_CHOICE and "options" in kwargs:
        kwargs["options"] = tuple(kwargs["options"])
    return config_cls(**kwargs)


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
