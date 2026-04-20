import type {
  FieldType,
  LongTextConfig,
  MultipleChoiceConfig,
  RatingConfig,
  ShortTextConfig,
  YesNoConfig,
} from '../types/fieldDefinition';

interface ShortTextConfigSnake {
  type: 'short_text';
  placeholder: string;
  max_length: number | null;
}

interface LongTextConfigSnake {
  type: 'long_text';
  placeholder: string;
  max_length: number | null;
}

interface MultipleChoiceConfigSnake {
  type: 'multiple_choice';
  options: string[];
  allow_multiple: boolean;
}

interface YesNoConfigSnake {
  type: 'yes_no';
  true_label: string;
  false_label: string;
}

interface RatingConfigSnake {
  type: 'rating';
  max_value: number;
  label: string;
}

export type FieldConfigResponse =
  | ShortTextConfigSnake
  | LongTextConfigSnake
  | MultipleChoiceConfigSnake
  | YesNoConfigSnake
  | RatingConfigSnake;

export type FieldConfigCamel =
  | ShortTextConfig
  | LongTextConfig
  | MultipleChoiceConfig
  | YesNoConfig
  | RatingConfig;

export function configResponseToCamel(
  response: FieldConfigResponse,
): FieldConfigCamel {
  switch (response.type) {
    case 'short_text':
      return {
        placeholder: response.placeholder,
        maxLength: response.max_length,
      };
    case 'long_text':
      return {
        placeholder: response.placeholder,
        maxLength: response.max_length,
      };
    case 'multiple_choice':
      return {
        options: response.options,
        allowMultiple: response.allow_multiple,
      };
    case 'yes_no':
      return {
        trueLabel: response.true_label,
        falseLabel: response.false_label,
      };
    case 'rating':
      return { maxValue: response.max_value, label: response.label };
  }
}

export function configToSnakeRequest(
  type: FieldType,
  config: FieldConfigCamel,
): FieldConfigResponse {
  switch (type) {
    case 'short_text': {
      const c = config as ShortTextConfig;
      return { type, placeholder: c.placeholder, max_length: c.maxLength };
    }
    case 'long_text': {
      const c = config as LongTextConfig;
      return { type, placeholder: c.placeholder, max_length: c.maxLength };
    }
    case 'multiple_choice': {
      const c = config as MultipleChoiceConfig;
      return { type, options: c.options, allow_multiple: c.allowMultiple };
    }
    case 'yes_no': {
      const c = config as YesNoConfig;
      return { type, true_label: c.trueLabel, false_label: c.falseLabel };
    }
    case 'rating': {
      const c = config as RatingConfig;
      return { type, max_value: c.maxValue, label: c.label };
    }
  }
}
