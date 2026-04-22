# GS-Typeforms
A typeform like application

## Running application dev environment

You can run the dev environment two ways:

- **[Docker Compose](#running-with-docker-compose)** — one command, no local Python/Node setup required.
- **[Local (uv + npm)](#python-api-application)** — run the API and UI directly on your machine.

## Running with Docker Compose

The easiest way to get both services up and running. Requires [Docker](https://docs.docker.com/get-docker/) (Desktop on Mac/Windows, Engine on Linux).

### Start the dev environment

From the repository root:

```bash
docker compose up --build
```

This uses `docker-compose.yml` + `docker-compose.override.yml` together, giving you:

- UI at `http://localhost:5173` (Vite dev server with hot module replacement)
- API at `http://localhost:8000` (uvicorn with `--reload`)
- API interactive docs at `http://localhost:8000/docs`

Source code is bind-mounted into both containers, so local edits trigger reloads automatically. SQLite data persists in a named Docker volume (`db_data`).

To stop the services:

```bash
docker compose down           # stop containers
docker compose down -v        # stop containers and delete the db volume
```

### Exec into a running container

```bash
# API (Debian-based)
docker compose exec api bash

# UI (Alpine-based — use sh, not bash)
docker compose exec ui sh
```

If a container has crashed and you want a fresh one-off shell:

```bash
docker compose run --rm --entrypoint="" api bash
```

### Tailing logs

View logs streamed from the containers (all services):

```bash
docker compose logs -f
```

Tail logs for a single service:

```bash
docker compose logs -f api
docker compose logs -f ui
```

The API also writes rotating file logs inside the container at `/app/apps/rest-api/src/logs/typeforms-dev.log`. Since the `logs/` directory is not mounted to the host, tail it through Docker:

```bash
docker compose exec api tail -f apps/rest-api/src/logs/typeforms-dev.log
```

### Running in production mode

The override file is only applied automatically — opt out of it to run the built (non-reload) production images:

```bash
docker compose -f docker-compose.yml up --build
```

In this mode the UI is served by nginx on `http://localhost` (port 80), and the API runs without reload.

## Running locally (without Docker)

### Python API Application

#### 1. Install uv

[uv](https://docs.astral.sh/uv/) is the Python package and project manager used by this project.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal (or run `source $HOME/.local/bin/env`) so `uv` is on your `PATH`.

#### 2. Install Python

The API requires Python ≥ 3.14. Use uv to install it:

```bash
uv python install 3.14
```

#### 3. Install dependencies

From the `api/` directory, install all workspace packages and dev dependencies:

```bash
cd api
uv sync --all-packages
```

#### 4. Run the dev server

```bash
uv run rest-api
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

#### 5. Other commands

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest path/to/test_file.py

# Lint source files
uv run ruff check .

# Format source files
uv run ruff format .

# Type-check source files
uv run ty check
```

### TypeScript/React UI Application

#### 1. Install Node.js

Use [nvm](https://github.com/nvm-sh/nvm) (Node Version Manager) to install and manage Node.js:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Restart your terminal, then install the latest LTS release of Node.js:

```bash
nvm install --lts
nvm use --lts
```

This also installs `npm`.

#### 2. Install dependencies

From the `ui/` directory, install all packages:

```bash
cd ui
npm install
```

#### 3. Run the dev server

```bash
npm run dev
```

The app will be available at `http://localhost:5173` with hot module replacement enabled.

#### 4. Other commands

```bash
# Lint source files
npm run lint

# Type-check source files (no output files emitted)
npm run ts-check

# Build for production (type-checks + bundles)
npm run build

# Preview the production build locally
npm run preview
```