FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src
COPY tests/ ./tests

EXPOSE 8022

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8022"]
