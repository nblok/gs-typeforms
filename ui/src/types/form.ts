import type { FormField } from '../pages/FormBuilder/formField';

export interface FormSummary {
  id: string;
  title: string;
  createdAt: string | null;
}

export interface Form {
  id: string;
  title: string;
  fields: FormField[];
  createdAt: string | null;
  modifiedAt: string | null;
}

export interface CreateFormPayload {
  title: string;
  fields: FormField[];
}
