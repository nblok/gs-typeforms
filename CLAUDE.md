# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

A Typeform-style form builder application built for a Greenspace Health engineering interview. It has a Python backend API and a React/TypeScript frontend. Most packages are stubs — this is intentionally early-stage.

## Architecture

Two top-level directories:

- `api/` — Python backend, managed as a **uv workspace** (Python ≥ 3.14)
- `ui/` — React 19 + TypeScript frontend built with Vite

### Backend (`api/`)

The workspace is structured as internal packages under `api/`:

| Package | Path | Purpose |
|---|---|---|
| `rest-api` | `apps/rest-api/` | Entrypoint / HTTP layer |
| `typeforms-domain` | `packages/typeforms-domain/` | Domain model / business logic |
| `typeforms-domain-dataaccess` | `packages/typeforms-domain-dataaccess/` | Data access / persistence |
| `common` | `packages/common/` | Shared utilities |

The intended dependency direction is: `rest-api` → `typeforms-domain` → `typeforms-domain-dataaccess`, with `common` usable by all layers. Each package's source lives under `src/<package_name>/`.

Dev tooling (ruff, pytest, ty) is declared in the root `api/pyproject.toml` dev dependency group, not in individual packages.

### Frontend (`ui/`)

Standard Vite + React 19 scaffold with TypeScript. Currently a default Vite starter — no routing, state management, or API integration yet.

## Coding Standards

- **API (backend):** [`docs/api.md`](docs/api.md) — architecture, DDD patterns, naming conventions, DI, logging, and testing standards for the `api/` workspace.
- **UI (frontend):** [`docs/ui.md`](docs/ui.md) — component conventions, routing, data fetching, date formatting, naming conventions, and testing standards for the `ui/` application.

## Commands

### Backend (run from `api/`)

```bash
# Install all workspace packages + dev deps
uv sync

# Run linter
uv run ruff check .

# Run type checker
uv run ty check

# Run tests
uv run pytest

# Run a single test file
uv run pytest path/to/test_file.py

# Run the REST API
uv run rest-api
```

### Frontend (run from `ui/`)

```bash
npm install        # install deps
npm run dev        # dev server with HMR
npm run build      # type-check + production build
npm run lint       # ESLint
npm run preview    # preview production build
```