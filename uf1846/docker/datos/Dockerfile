# docker/datos/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY datos/app.py .
COPY datos/config.py .

# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Запускаем приложение на порту 5003
EXPOSE 5003

CMD ["python", "app.py"]