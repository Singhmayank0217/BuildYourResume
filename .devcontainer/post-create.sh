#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/smart-resume-builder/backend

export DATABASE_URL="${DATABASE_URL:-postgresql://smart:smart@postgres:5432/smart_resume}"
export REDIS_URL="${REDIS_URL:-redis://redis:6379/0}"
export CELERY_BROKER_URL="${CELERY_BROKER_URL:-redis://redis:6379/0}"
export JWT_SECRET="${JWT_SECRET:-change-me}"
export LLM_PROVIDER="${LLM_PROVIDER:-local}"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if command -v alembic >/dev/null 2>&1; then
  alembic upgrade head || true
fi

if [ -d tests ]; then
  pytest -q || true
fi
