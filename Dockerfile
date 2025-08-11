FROM python:3.9-slim as base
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl git && rm -rf /var/lib/apt/lists/*
RUN useradd -ms /bin/bash appuser
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY scripts/ ./scripts/
RUN mkdir -p /app/data/documents /app/logs
RUN chown -R appuser:appuser /app/data /app/logs
USER appuser
