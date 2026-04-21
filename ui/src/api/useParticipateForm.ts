import { useQuery } from '@tanstack/react-query';
import { getFormForParticipation } from './responses';

export function useParticipateForm(formId: string | undefined) {
  return useQuery({
    queryKey: ['participate-form', formId],
    queryFn: () => getFormForParticipation(formId!),
    enabled: Boolean(formId),
  });
}
