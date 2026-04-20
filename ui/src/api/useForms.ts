import { useQuery } from '@tanstack/react-query';
import { getForms } from './forms';

export function useForms() {
  return useQuery({
    queryKey: ['forms'],
    queryFn: getForms,
  });
}
