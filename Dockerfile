# syntax=docker/dockerfile:1
FROM python:3.10-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgomp1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- training image (default) ----
FROM base AS train
COPY . .
CMD ["python", "scripts/train.py", "--config", "configs/experiments.yaml"]

# ---- API image (Phase 3; requires app/main) ----
FROM base AS api
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
