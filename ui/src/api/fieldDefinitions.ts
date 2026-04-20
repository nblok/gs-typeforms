import { apiClient } from './client';
import type {
  FieldDefinition,
  FieldType,
  LongTextConfig,
  MultipleChoiceConfig,
  RatingConfig,
  ShortTextConfig,
  YesNoConfig,
} from '../types/fieldDefinition';

interface ShortTextConfigResponse {
  type: 'short_text';
  placeholder: string;
  max_length: number | null;
}

interface LongTextConfigResponse {
  type: 'long_text';
  placeholder: string;
  max_length: number | null;
}

interface MultipleChoiceConfigResponse {
  type: 'multiple_choice';
  options: string[];
  allow_multiple: boolean;
}

interface YesNoConfigResponse {
  type: 'yes_no';
  true_label: string;
  false_label: string;
}

interface RatingConfigResponse {
  type: 'rating';
  max_value: number;
  label: string;
}

type FieldConfigResponse =
  | ShortTextConfigResponse
  | LongTextConfigResponse
  | MultipleChoiceConfigResponse
  | YesNoConfigResponse
  | RatingConfigResponse;

interface FieldDefinitionResponse {
  type: FieldType;
  label: string;
  description: string;
  icon: string;
  default_config: FieldConfigResponse;
}

function toShortTextConfig(c: ShortTextConfigResponse): ShortTextConfig {
  return { placeholder: c.placeholder, maxLength: c.max_length };
}

function toLongTextConfig(c: LongTextConfigResponse): LongTextConfig {
  return { placeholder: c.placeholder, maxLength: c.max_length };
}

function toMultipleChoiceConfig(c: MultipleChoiceConfigResponse): MultipleChoiceConfig {
  return { options: c.options, allowMultiple: c.allow_multiple };
}

function toYesNoConfig(c: YesNoConfigResponse): YesNoConfig {
  return { trueLabel: c.true_label, falseLabel: c.false_label };
}

function toRatingConfig(c: RatingConfigResponse): RatingConfig {
  return { maxValue: c.max_value, label: c.label };
}

function toFieldDefinition(dto: FieldDefinitionResponse): FieldDefinition {
  const base = { label: dto.label, description: dto.description, icon: dto.icon };
  switch (dto.default_config.type) {
    case 'short_text':
      return { ...base, type: 'short_text', defaultConfig: toShortTextConfig(dto.default_config) };
    case 'long_text':
      return { ...base, type: 'long_text', defaultConfig: toLongTextConfig(dto.default_config) };
    case 'multiple_choice':
      return {
        ...base,
        type: 'multiple_choice',
        defaultConfig: toMultipleChoiceConfig(dto.default_config),
      };
    case 'yes_no':
      return { ...base, type: 'yes_no', defaultConfig: toYesNoConfig(dto.default_config) };
    case 'rating':
      return { ...base, type: 'rating', defaultConfig: toRatingConfig(dto.default_config) };
  }
}

export async function getFieldDefinitions(): Promise<FieldDefinition[]> {
  const response = await apiClient.get<FieldDefinitionResponse[]>('/field-definitions/');
  return response.data.map(toFieldDefinition);
}
