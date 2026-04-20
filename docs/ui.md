# UI Coding Standards

This document defines the coding standards and architectural conventions for the `ui/` frontend application.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Components](#components)
4. [Routing](#routing)
5. [Data Fetching](#data-fetching)
6. [Date Formatting](#date-formatting)
7. [Naming Conventions](#naming-conventions)
8. [Code Style](#code-style)
9. [Testing](#testing)
10. [Linting](#linting)

---

## Architecture Overview

The frontend is a React 19 + TypeScript single-page application built with Vite. It communicates with the backend REST API exclusively via TanStack React Query and axios.

```
ui/src/
├── pages/          ← Route-level components (one per route)
├── components/     ← Shared presentational components
├── api/            ← Axios client + React Query hooks
├── types/          ← Shared TypeScript types and interfaces
└── main.tsx        ← App entry point with router and query client setup
```

---

## Directory Structure

| Path | Purpose |
|---|---|
| `src/pages/` | Route-level page components |
| `src/components/` | Shared components used across multiple pages |
| `src/api/` | Axios instance, API functions, and React Query hooks |
| `src/types/` | Shared TypeScript type and interface definitions |

Page components are co-located with their route. Each page directory may contain page-specific child components that are not shared elsewhere:

```
src/pages/
└── FormBuilder/
    ├── FormBuilderPage.tsx     ← Route component
    └── FieldList.tsx           ← Page-specific child (not shared)
```

---

## Components

Use **Material-UI (MUI) components exclusively**. Do not create custom styled components or wrapper components around MUI primitives.

```tsx
// Correct — use MUI directly
import { Box, Button, TextField, Typography } from '@mui/material';

function MyForm() {
  return (
    <Box component="form">
      <Typography variant="h5">Create Form</Typography>
      <TextField label="Title" fullWidth />
      <Button variant="contained" type="submit">Save</Button>
    </Box>
  );
}
```

```tsx
// Incorrect — do not wrap MUI in custom components
function PrimaryButton({ children }: { children: React.ReactNode }) {
  return <Button variant="contained">{children}</Button>;
}
```

**Rules:**
- Use MUI layout components (`Box`, `Stack`, `Grid`) for all layout.
- Use MUI typography variants (`h1`–`h6`, `body1`, `body2`, `caption`, etc.) — do not use raw HTML heading or paragraph tags.
- Use MUI `sx` prop for one-off style overrides. Do not write CSS files or use inline `style` attributes.
- Use the MUI theme for colours and spacing. Do not hardcode hex values or pixel sizes outside the theme.
- Use MUI `CircularProgress` for loading states and MUI `Alert` for error states.

---

## Routing

Use `react-router-dom` for all client-side routing.

Define routes in a single file at `src/routes.tsx`. Use `createBrowserRouter` and `RouterProvider`.

```tsx
// src/routes.tsx
import { createBrowserRouter } from 'react-router-dom';
import { FormsListPage } from './pages/FormsList/FormsListPage';
import { FormBuilderPage } from './pages/FormBuilder/FormBuilderPage';

export const router = createBrowserRouter([
  { path: '/', element: <FormsListPage /> },
  { path: '/forms/:formId', element: <FormBuilderPage /> },
]);
```

```tsx
// src/main.tsx
import { RouterProvider } from 'react-router-dom';
import { router } from './routes';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
);
```

Use `useNavigate` for programmatic navigation and `useParams` to read route parameters. Do not use the `<a>` tag for internal links — use MUI's `<Link component={RouterLink}>` pattern.

---

## Data Fetching

Use **TanStack React Query** for all server state. Use **axios** for HTTP requests. Do not use `fetch` directly.

### Axios Client

Define a single axios instance in `src/api/client.ts`:

```ts
// src/api/client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
});
```

### API Functions

Define plain async functions per resource in `src/api/`. Each file maps to one backend resource.

```ts
// src/api/forms.ts
import { apiClient } from './client';
import type { Form, CreateFormPayload } from '../types/form';

export async function getForms(): Promise<Form[]> {
  const response = await apiClient.get<Form[]>('/forms');
  return response.data;
}

export async function createForm(payload: CreateFormPayload): Promise<Form> {
  const response = await apiClient.post<Form>('/forms', payload);
  return response.data;
}
```

### React Query Hooks

Wrap API functions in custom hooks, co-located with their API file or in a dedicated `hooks/` subdirectory under `src/api/`.

```ts
// src/api/useForms.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getForms, createForm } from './forms';

export function useForms() {
  return useQuery({ queryKey: ['forms'], queryFn: getForms });
}

export function useCreateForm() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createForm,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['forms'] }),
  });
}
```

**Rules:**
- Query keys must be arrays. Use the resource name as the first element, followed by any IDs or filters.
- Always invalidate relevant query keys after a successful mutation.
- Use `isPending`, `isError`, and `data` from query/mutation results — do not maintain local loading or error state for server operations.
- Initialise `QueryClient` once in `main.tsx`. Do not create `QueryClient` instances inside components.

---

## Date Formatting

Use **date-fns** for all date formatting. Do not use `Date.toLocaleDateString()` or any other formatting method.

Format dates using ordinal day, abbreviated month, and full year:

| Date | Formatted output |
|---|---|
| 2025-09-01 | 1st Sep 2025 |
| 2025-08-02 | 2nd Aug 2025 |
| 2026-01-03 | 3rd Jan 2026 |
| 2024-07-04 | 4th Jul 2024 |

Use the `do MMM yyyy` format string with `format` from date-fns:

```ts
import { format } from 'date-fns';

function formatDate(date: Date | string): string {
  return format(new Date(date), 'do MMM yyyy');
}
```

Define this utility in `src/utils/formatDate.ts` and import it wherever dates are displayed.

---

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Component file | `PascalCase.tsx` | `FormBuilderPage.tsx` |
| Hook file | `camelCase.ts`, prefixed `use` | `useForms.ts` |
| API function file | `camelCase.ts` (resource noun) | `forms.ts` |
| Type / interface file | `camelCase.ts` | `form.ts` |
| Utility file | `camelCase.ts` | `formatDate.ts` |
| Component | `PascalCase` | `FormBuilderPage` |
| Hook | `use` + `PascalCase` | `useForms`, `useCreateForm` |
| Type / interface | `PascalCase` | `Form`, `CreateFormPayload` |
| Query key | Resource noun, plural | `['forms']`, `['forms', formId]` |
| Env variable | `VITE_` prefix, `SCREAMING_SNAKE_CASE` | `VITE_API_BASE_URL` |

---

## Code Style

- **TypeScript**: strict mode enabled. All props, function parameters, and return types must be typed.
- **`interface` vs `type`**: Use `interface` for object shapes (props, API payloads). Use `type` for unions and aliases.
- **Props**: Define a `Props` interface in the same file as the component. Do not use `React.FC` — declare the function signature directly.

```tsx
interface Props {
  formId: string;
  onSave: (title: string) => void;
}

function FormHeader({ formId, onSave }: Props) { ... }
```

- **Imports**: Group in order — external packages, then internal modules. Use path aliases (e.g. `@/`) if configured in `tsconfig`.
- **Default exports**: Use named exports for all components, hooks, and utilities. Default exports are only used for pages (to support lazy loading if needed).
- **Comments**: Avoid unless explaining a non-obvious constraint or workaround. Do not write JSDoc on obvious components or utilities.
- **`null` vs `undefined`**: Prefer `undefined` for optional values. Use `null` only when required by a third-party API.

---

## Testing

Use **vitest** for all tests. Co-locate test files with their source using a `.test.ts` / `.test.tsx` suffix.

```
src/api/
├── forms.ts
└── forms.test.ts

src/utils/
├── formatDate.ts
└── formatDate.test.ts
```

**Rules:**
- Group related tests in `describe` blocks named after the function or component under test.
- Name test cases `it('should <expected behaviour> when <condition>')`.
- Test React Query hooks with a wrapper that provides a `QueryClient`.
- Do not test MUI rendering internals — test behaviour visible to the user (text content, button clicks, form submissions).
- Mock the axios `apiClient` at the module boundary, not individual axios methods.

```ts
// Example utility test
import { describe, it, expect } from 'vitest';
import { formatDate } from './formatDate';

describe('formatDate', () => {
  it('should format date with ordinal day, abbreviated month and full year', () => {
    expect(formatDate('2025-09-01')).toBe('1st Sep 2025');
    expect(formatDate('2025-08-02')).toBe('2nd Aug 2025');
  });
});
```

---

## Linting

Use **ESLint** with the project's `eslint.config.js`. Run from `ui/`:

```bash
npm run lint
```

All lint errors must be resolved before committing. Do not use `// eslint-disable` comments unless there is a documented reason that cannot be addressed by changing the code.
