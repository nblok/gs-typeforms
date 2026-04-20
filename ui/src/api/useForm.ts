import { useQuery } from '@tanstack/react-query';
import { getForm } from './forms';

export function useForm(formId: string | undefined) {
  return useQuery({
    queryKey: ['forms', formId],
    queryFn: () => getForm(formId!),
    enabled: Boolean(formId),
  });
}
