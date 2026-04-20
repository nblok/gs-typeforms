export type FieldType =
  | 'short_text'
  | 'long_text'
  | 'multiple_choice'
  | 'yes_no'
  | 'rating';

export interface ShortTextConfig {
  placeholder: string;
  maxLength: number | null;
}

export interface LongTextConfig {
  placeholder: string;
  maxLength: number | null;
}

export interface MultipleChoiceConfig {
  options: string[];
  allowMultiple: boolean;
}

export interface YesNoConfig {
  trueLabel: string;
  falseLabel: string;
}

export interface RatingConfig {
  maxValue: number;
  label: string;
}

interface BaseFieldDefinition {
  label: string;
  description: string;
  icon: string;
}

export type FieldDefinition =
  | (BaseFieldDefinition & { type: 'short_text'; defaultConfig: ShortTextConfig })
  | (BaseFieldDefinition & { type: 'long_text'; defaultConfig: LongTextConfig })
  | (BaseFieldDefinition & { type: 'multiple_choice'; defaultConfig: MultipleChoiceConfig })
  | (BaseFieldDefinition & { type: 'yes_no'; defaultConfig: YesNoConfig })
  | (BaseFieldDefinition & { type: 'rating'; defaultConfig: RatingConfig });
