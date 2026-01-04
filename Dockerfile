FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m textblob.download_corpora

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]