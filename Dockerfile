FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/src ./src
COPY app/tests ./tests

FROM builder AS test

WORKDIR /app
RUN pytest tests

FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src ./src

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "src.app"]
