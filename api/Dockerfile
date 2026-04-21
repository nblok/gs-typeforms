FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY apps/ apps/
COPY packages/ packages/

RUN uv sync --frozen --no-dev --all-packages && \
    mkdir -p apps/rest-api/src/db apps/rest-api/src/logs

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "rest_api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]
