FROM python:3.15-slim

WORKDIR /app

COPY docker/requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY src/ ./src/

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]