import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  getResponseByRespondent,
  getResponsesForForm,
  submitResponse,
} from './responses';
import type { SubmitResponsePayload } from '../types/response';

export function useResponse(
  formId: string | undefined,
  respondentId: string | undefined,
) {
  return useQuery({
    queryKey: ['responses', formId, respondentId],
    queryFn: () => getResponseByRespondent(formId!, respondentId!),
    enabled: Boolean(formId) && Boolean(respondentId),
  });
}

export function useResponsesForForm(formId: string | undefined) {
  return useQuery({
    queryKey: ['responses', formId],
    queryFn: () => getResponsesForForm(formId!),
    enabled: Boolean(formId),
  });
}

export function useSubmitResponse(formId: string | undefined) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: SubmitResponsePayload) =>
      submitResponse(formId!, payload),
    onSuccess: (data) => {
      queryClient.setQueryData(
        ['responses', formId, data.respondentId],
        data,
      );
    },
  });
}
