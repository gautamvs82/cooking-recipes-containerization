FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OLLAMA_URL=http://host.docker.internal:11434 \
    OLLAMA_MODEL=qwen3:0.6b

WORKDIR /app
COPY chat.py /app/chat.py

# Keep the container running so you can enter it later with docker exec.
CMD ["sh", "-c", "while :; do sleep 3600; done"]
