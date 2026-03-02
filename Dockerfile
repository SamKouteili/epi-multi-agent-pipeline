FROM python:3.11-slim

# Node.js 20 (required by claude-code-sdk)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Claude CLI
RUN npm install -g @anthropic-ai/claude-code

# Env vars for headless Claude CLI inside container
ENV NODE_PATH="/usr/local/lib/node_modules"
ENV DISABLE_AUTOUPDATER=1
ENV NODE_ENV=production

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir . gradio

EXPOSE 7860

CMD ["python", "web/app.py"]
