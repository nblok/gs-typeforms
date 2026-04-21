import { apiClient } from './client';
import {
  configResponseToCamel,
  type FieldConfigResponse,
} from './fieldConfigMappers';
import type { FieldType } from '../types/fieldDefinition';
import type {
  AnswerValue,
  FormResponse,
  ParticipateForm,
  SubmitResponsePayload,
} from '../types/response';

interface FormFieldResponse {
  id: string;
  label: string;
  field_type: FieldType;
  order: number;
  required: boolean;
  config: FieldConfigResponse;
}

interface FormResponseBody {
  id: string;
  title: string;
  fields: FormFieldResponse[];
  created_at: string | null;
  modified_at: string | null;
}

interface FormResponseApi {
  id: string;
  form_id: string;
  respondent_id: string;
  answers: Record<string, AnswerValue>;
  submitted_at: string | null;
  modified_at: string | null;
}

function toParticipateForm(response: FormResponseBody): ParticipateForm {
  return {
    id: response.id,
    title: response.title,
    fields: response.fields.map(
      (f) =>
        ({
          id: f.id,
          label: f.label,
          type: f.field_type,
          order: f.order,
          required: f.required,
          config: configResponseToCamel(f.config),
        }) as ParticipateForm['fields'][number],
    ),
  };
}

function toFormResponse(body: FormResponseApi): FormResponse {
  return {
    id: body.id,
    formId: body.form_id,
    respondentId: body.respondent_id,
    answers: body.answers,
    submittedAt: body.submitted_at,
    modifiedAt: body.modified_at,
  };
}

export async function getFormForParticipation(
  formId: string,
): Promise<ParticipateForm> {
  const response = await apiClient.get<FormResponseBody>(`/forms/${formId}`);
  return toParticipateForm(response.data);
}

export async function getResponseByRespondent(
  formId: string,
  respondentId: string,
): Promise<FormResponse | null> {
  const response = await apiClient.get<FormResponseApi | null>(
    `/forms/${formId}/responses/respondents/${respondentId}`,
  );
  return response.data ? toFormResponse(response.data) : null;
}

export async function submitResponse(
  formId: string,
  payload: SubmitResponsePayload,
): Promise<FormResponse> {
  const body = {
    respondent_id: payload.respondentId,
    answers: payload.answers,
  };
  const response = await apiClient.post<FormResponseApi>(
    `/forms/${formId}/responses`,
    body,
  );
  return toFormResponse(response.data);
}
