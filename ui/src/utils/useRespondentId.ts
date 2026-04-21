import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';

const RESPONDENT_ID_KEY = 'respondentId';

export function useRespondentId(): [string, () => void] {
  const [id, setId] = useLocalStorage<string>(RESPONDENT_ID_KEY, '');

  useEffect(() => {
    if (!id) setId(crypto.randomUUID());
  }, [id, setId]);

  const regenerate = () => setId(crypto.randomUUID());

  return [id, regenerate];
}
