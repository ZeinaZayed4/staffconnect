FROM python:3.11.18-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser \
    && mkdir -p /app/media \
    && chown -R appuser:appuser /app \
    && chmod +x /app/entrypoint.sh

USER appuser

VOLUME /app/media

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
