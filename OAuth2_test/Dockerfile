FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Хост микросервиса авторизации.
ENV AUTH_SERVER_HOST="localhost"
# Порт микросервиса авторизации.
ENV AUTH_SERVER_PORT=8001

WORKDIR /app

COPY .  /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
