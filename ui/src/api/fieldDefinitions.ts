import { apiClient } from './client';
import {
  configResponseToCamel,
  type FieldConfigResponse,
} from './fieldConfigMappers';
import type { FieldDefinition, FieldType } from '../types/fieldDefinition';

interface FieldDefinitionResponse {
  type: FieldType;
  label: string;
  description: string;
  icon: string;
  default_config: FieldConfigResponse;
}

function toFieldDefinition(dto: FieldDefinitionResponse): FieldDefinition {
  const base = { label: dto.label, description: dto.description, icon: dto.icon };
  const defaultConfig = configResponseToCamel(dto.default_config);
  switch (dto.default_config.type) {
    case 'short_text':
    case 'long_text':
    case 'multiple_choice':
    case 'yes_no':
    case 'rating':
      return {
        ...base,
        type: dto.default_config.type,
        defaultConfig,
      } as FieldDefinition;
  }
}

export async function getFieldDefinitions(): Promise<FieldDefinition[]> {
  const response = await apiClient.get<FieldDefinitionResponse[]>(
    '/field-definitions/',
  );
  return response.data.map(toFieldDefinition);
}
