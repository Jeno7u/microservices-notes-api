#!/bin/sh
# set -e

# alembic -c /workspace/notes/alembic.ini revision --autogenerate -m "Notes init migrate"

alembic -c /workspace/notes/alembic.ini upgrade head

cd /workspace

exec uvicorn notes.app.main:app --host 0.0.0.0 --port 8000
