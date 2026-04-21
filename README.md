# GS-Typeforms
A typeform like application

## Running application dev environment
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
uv sync
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