FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r /app/requirements.txt

COPY app /app/app

FROM python:3.12-slim AS test

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app /app/app

WORKDIR /app/app

RUN pytest || (echo "Tests failed" && exit 1)

FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app /app/app

ENV PYTHONPATH=/app

WORKDIR /app/app

CMD ["python", "-m", "src.app"]