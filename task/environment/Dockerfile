FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY renderer/ /app/renderer/

RUN mkdir -p /app/output

WORKDIR /app/renderer

CMD ["python", "main.py"]
