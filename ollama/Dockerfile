FROM ollama/ollama

# Download the model while building the image.
RUN ollama serve & \
    pid=$!; \
    for i in $(seq 1 60); do \
      if ollama list >/dev/null 2>&1; then break; fi; \
      sleep 1; \
    done; \
    ollama pull qwen3:0.6b; \
    kill $pid; \
    wait $pid || true