FROM python:3.13.10-slim

# copiamos uv desde imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

# copiar primero dependencias (mejor cache)
COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --locked

# copiar código
COPY pipeline/pipeline.py pipeline.py

ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
