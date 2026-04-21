import { useCallback, useEffect, useState } from 'react';

type Listener = () => void;
const listenersByKey: Record<string, Set<Listener>> = {};

function subscribe(key: string, listener: Listener): () => void {
  const set = listenersByKey[key] ?? (listenersByKey[key] = new Set());
  set.add(listener);
  return () => set.delete(listener);
}

function notify(key: string): void {
  listenersByKey[key]?.forEach((l) => l());
}

function readValue<T>(key: string, initial: T): T {
  if (typeof window === 'undefined') return initial;
  const raw = window.localStorage.getItem(key);
  if (raw === null) return initial;
  try {
    return JSON.parse(raw) as T;
  } catch {
    return initial;
  }
}

export function useLocalStorage<T>(
  key: string,
  initial: T,
): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(() => readValue(key, initial));

  const update = useCallback(
    (next: T) => {
      window.localStorage.setItem(key, JSON.stringify(next));
      notify(key);
    },
    [key],
  );

  useEffect(() => {
    const resync = () => setValue(readValue(key, initial));
    const unsubscribe = subscribe(key, resync);
    const onStorage = (e: StorageEvent) => {
      if (e.key === key) resync();
    };
    window.addEventListener('storage', onStorage);
    return () => {
      unsubscribe();
      window.removeEventListener('storage', onStorage);
    };
  }, [key, initial]);

  return [value, update];
}
