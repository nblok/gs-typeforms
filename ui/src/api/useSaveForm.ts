import { useMutation, useQueryClient } from '@tanstack/react-query';
import { saveForm } from './forms';

export function useSaveForm() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: saveForm,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['forms'] }),
  });
}
