import type {
  LongTextConfig,
  MultipleChoiceConfig,
  RatingConfig,
  ShortTextConfig,
  YesNoConfig,
} from '../../types/fieldDefinition';

interface BaseFormField {
  id: number;
  label: string;
  required: boolean;
}

export type FormField =
  | (BaseFormField & { type: 'short_text'; config: ShortTextConfig })
  | (BaseFormField & { type: 'long_text'; config: LongTextConfig })
  | (BaseFormField & { type: 'multiple_choice'; config: MultipleChoiceConfig })
  | (BaseFormField & { type: 'yes_no'; config: YesNoConfig })
  | (BaseFormField & { type: 'rating'; config: RatingConfig });
