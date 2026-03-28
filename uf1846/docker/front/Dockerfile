# docker/front/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код и шаблоны
COPY front/app.py .
COPY front/script_generar_hash.py .
COPY front/templates ./templates

# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Запускаем приложение на порту 5001
EXPOSE 5001

CMD ["python", "app.py"]