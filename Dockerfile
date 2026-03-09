FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir . gradio

# v2: 58 indicators + Reports tab + pipeline outputs
EXPOSE 7860

CMD ["python", "web/app.py"]
