FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Время жизни токена доступа.
ENV ACCESS_TOKEN_EXPIRE_MINUTES=10
# Время жизни токена обновления.
ENV REFRESH_TOKEN_EXPIRE_MINUTES=60
# Соединение с базой данных.
ENV DB_CONNECT_STR="sqlite:///db.sqlite3"

# Пароли для пользователей при инициализации базы данных.
ENV INIT_ADMIN_PASSWORD="Pups_555"
ENV INIT_SYSTEM_PASSWORD="Pups_555"
ENV INIT_DIRECTOR_PASSWORD="Pups_555"
ENV INIT_USER_PASSWORD="Pups_555"

ENV DEBUG_MODE="True"

WORKDIR /app

COPY .  /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN alembic upgrade head

EXPOSE 8001

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
