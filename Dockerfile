# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://localhost:8080/health || exit 1

CMD ["uvicorn", "src.publishing.main:app", "--host", "0.0.0.0", "--port", "8080"]
