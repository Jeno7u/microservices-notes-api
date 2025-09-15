#!/bin/sh
# set -e

# alembic -c /workspace/auth/alembic.ini revision --autogenerate -m "Auth init migrate"

alembic -c /workspace/auth/alembic.ini upgrade head

cd /workspace

exec uvicorn auth.app.main:app --host 0.0.0.0 --port 8000


