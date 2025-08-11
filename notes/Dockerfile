FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl build-essential

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /workspace

RUN mkdir -p notes

COPY notes/pyproject.toml notes/poetry.lock* /workspace/notes

WORKDIR /workspace/notes

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --only main

WORKDIR /workspace

COPY notes /workspace/notes

ENV PYTHONPATH="/workspace"

CMD ["uvicorn", "notes.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
