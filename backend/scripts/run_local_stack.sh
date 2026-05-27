#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.full.yml"

echo "Using compose file: $COMPOSE_FILE"
cd "$ROOT_DIR"

echo "Bringing up required services..."
docker compose -f "$COMPOSE_FILE" up -d postgres redis api celery-worker celery-beat flower

# Wait for Postgres to be healthy
echo "Waiting for Postgres to be ready..."
until docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U smart -d smart_resume >/dev/null 2>&1; do
  sleep 1
  echo -n "."
done

echo

echo "Running Alembic migrations inside api container..."
# Try running alembic upgrade; if Alembic missing, fallback to SQLAlchemy create_all
if docker compose -f "$COMPOSE_FILE" exec -T api alembic upgrade head; then
  echo "Alembic migrations applied"
else
  echo "Alembic failed or not available; attempting metadata.create_all fallback"
  docker compose -f "$COMPOSE_FILE" exec -T api python -c "from app.db.session import Base, engine; Base.metadata.create_all(bind=engine)"
fi

echo "Gathering logs (last 200 lines) from services..."
docker compose -f "$COMPOSE_FILE" logs --no-color --tail=200 api celery-worker celery-beat postgres redis flower > "$ROOT_DIR/stack_logs.txt"

echo "Logs saved to $ROOT_DIR/stack_logs.txt"

echo "To run integration tests: docker compose -f $COMPOSE_FILE exec -T api pytest -q"

echo "All done."
