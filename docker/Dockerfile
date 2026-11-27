FROM python:3.15-slim

WORKDIR /app

COPY docker/requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY src/ ./src/

CMD ["python", "-m", "src.train"]