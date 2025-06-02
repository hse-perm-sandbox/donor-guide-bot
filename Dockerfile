FROM python:3.12-slim-bookworm AS base
WORKDIR /app
COPY poetry.lock pyproject.toml alembic.ini ./
RUN python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-interaction --no-ansi --no-root

FROM python:3.12-slim-bookworm
COPY --from=base /app /app
WORKDIR /app
COPY ./src /app/src
COPY ./migration /app/migration
COPY ./assets /app/assets
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

CMD [".venv/bin/python", "src/main.py"]
