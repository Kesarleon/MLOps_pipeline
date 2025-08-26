FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install -U pip && pip install -r requirements.txt

COPY service/ /app/service/
EXPOSE 8000
CMD ["sh", "-c", "uvicorn service.app:app --host 0.0.0.0 --port 8000"]