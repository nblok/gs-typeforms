import { apiClient } from './client';
import {
  configResponseToCamel,
  configToSnakeRequest,
  type FieldConfigResponse,
} from './fieldConfigMappers';
import type { FieldType } from '../types/fieldDefinition';
import type { CreateFormPayload, Form } from '../types/form';
import type { FormField } from '../pages/FormBuilder/formField';

interface FormFieldRequest {
  label: string;
  field_type: FieldType;
  order: number;
  required: boolean;
  config: FieldConfigResponse;
}

interface CreateFormRequest {
  title: string;
  fields: FormFieldRequest[];
}

interface CreateFormResponse {
  id: string;
}

interface FormFieldResponse {
  id: string;
  label: string;
  field_type: FieldType;
  order: number;
  required: boolean;
  config: FieldConfigResponse;
}

interface FormResponse {
  id: string;
  title: string;
  fields: FormFieldResponse[];
  created_at: string | null;
  modified_at: string | null;
}

let nextLocalFieldId = 1_000_000;

function toFormFieldRequest(field: FormField, order: number): FormFieldRequest {
  return {
    label: field.label,
    field_type: field.type,
    order,
    required: field.required,
    config: configToSnakeRequest(field.type, field.config),
  };
}

function toFormField(response: FormFieldResponse): FormField {
  const base = {
    id: nextLocalFieldId++,
    label: response.label,
    required: response.required,
  };
  const config = configResponseToCamel(response.config);
  return { ...base, type: response.field_type, config } as FormField;
}

function toForm(response: FormResponse): Form {
  return {
    id: response.id,
    title: response.title,
    fields: response.fields.map(toFormField),
    createdAt: response.created_at,
    modifiedAt: response.modified_at,
  };
}

export async function saveForm(payload: CreateFormPayload): Promise<{ id: string }> {
  const body: CreateFormRequest = {
    title: payload.title,
    fields: payload.fields.map((f, i) => toFormFieldRequest(f, i)),
  };
  const response = await apiClient.post<CreateFormResponse>('/forms/', body);
  return { id: response.data.id };
}

export async function getForm(formId: string): Promise<Form> {
  const response = await apiClient.get<FormResponse>(`/forms/${formId}`);
  return toForm(response.data);
}
