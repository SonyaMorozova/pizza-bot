FROM python:3.13-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY bot/ ./bot/

CMD ["python", "-m", "bot"]