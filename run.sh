#!/bin/bash
set -euo pipefail
if ! command -v docker &>/dev/null; then
  echo "Docker is not installed. Please install Docker." >&2
  exit 1
fi
if ! command -v docker-compose &>/dev/null; then
  echo "docker-compose is not installed. Please install docker-compose." >&2
  exit 1
fi
PROJECT_NAME="faq-rag-env"
DB_CONTAINER="chroma-db"
PROCESSOR_CONTAINER="doc-processor"
if [[ "$*" == *--fresh* ]]; then
  echo "Removing all containers and named volumes for a fresh deployment..."
  docker-compose down -v || true
else
  echo "Cleaning up any existing containers (preserving named volumes)..."
  docker-compose stop || true
  docker-compose rm -f || true
fi
echo "Starting persistent Chroma DB service..."
docker-compose up -d $DB_CONTAINER
echo "Waiting for Chroma DB on localhost:8000..."
NEXT_TRY=0
while ! nc -z localhost 8000; do
  if (( NEXT_TRY > 60 )); then
    echo "Chroma DB did not become ready in time." >&2
    docker-compose logs $DB_CONTAINER
    exit 2
  fi
  sleep 1
  ((NEXT_TRY++))
done
echo "Initiating document processing and database setup..."
docker-compose run --rm $PROCESSOR_CONTAINER python scripts/full_setup.py
if [ $? -eq 0 ]; then
  echo "\n✅ Environment initialized successfully!"
  echo "Chroma DB is running and the database is fully populated at localhost:8000."
else
  echo "\n❌ Environment initialization failed. Check logs for errors."
  exit 3
fi
