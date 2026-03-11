FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

COPY pyproject.toml pytest.ini uv.lock ./

RUN uv sync --frozen --no-install-project

COPY src ./src

RUN uv sync --frozen

RUN mkdir -p /app/data && chmod 777 /app/data

CMD ["uv", "run", "uvicorn", "src.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]