import type {
  LongTextConfig,
  MultipleChoiceConfig,
  RatingConfig,
  ShortTextConfig,
  YesNoConfig,
} from './fieldDefinition';

interface BaseParticipateFormField {
  id: string;
  label: string;
  order: number;
  required: boolean;
}

export type ParticipateFormField =
  | (BaseParticipateFormField & { type: 'short_text'; config: ShortTextConfig })
  | (BaseParticipateFormField & { type: 'long_text'; config: LongTextConfig })
  | (BaseParticipateFormField & {
      type: 'multiple_choice';
      config: MultipleChoiceConfig;
    })
  | (BaseParticipateFormField & { type: 'yes_no'; config: YesNoConfig })
  | (BaseParticipateFormField & { type: 'rating'; config: RatingConfig });

export interface ParticipateForm {
  id: string;
  title: string;
  fields: ParticipateFormField[];
}

export type AnswerValue = string | string[] | boolean | number;

export interface FormResponse {
  id: string;
  formId: string;
  respondentId: string;
  answers: Record<string, AnswerValue>;
  submittedAt: string | null;
  modifiedAt: string | null;
}

export interface SubmitResponsePayload {
  respondentId: string;
  answers: Record<string, AnswerValue>;
}
