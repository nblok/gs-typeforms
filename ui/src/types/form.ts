import type { FormField } from '../pages/FormBuilder/formField';

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
