import { useQuery } from '@tanstack/react-query';
import { getFieldDefinitions } from './fieldDefinitions';

export function useFieldDefinitions() {
  return useQuery({
    queryKey: ['fieldDefinitions'],
    queryFn: getFieldDefinitions,
  });
}
