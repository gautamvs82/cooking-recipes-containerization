# Ollama terminal client container

This is a small second image for entering a container shell and chatting with an existing Ollama server. It does not run Ollama or include a model; it sends requests to the Ollama API at port 11434.

## Build and start

In PowerShell, change to this folder and run:

```powershell
docker compose up --build -d
```

The default Ollama address is `http://host.docker.internal:11434`, which works when Ollama publishes port 11434 on the Windows host. Set `OLLAMA_URL` if the server is at another address. For example, if Ollama is another container on a shared Docker network, use its service or container name, such as `http://ollama:11434`, and attach this service to that same network.

## Enter the container and chat

```powershell
docker exec -it ollama-terminal sh
python /app/chat.py
```

Use `/reset` to clear the current conversation or `/exit` to end the chat. The container remains running until stopped, so you can leave the shell and enter it again with the same `docker exec` command. To stop and remove it:

```powershell
docker compose down
```

## Choose another model or API address

Create a `.env` file beside `compose.yaml`:

```dotenv
OLLAMA_URL=http://host.docker.internal:11434
OLLAMA_MODEL=qwen3:0.6b
```

Then recreate the helper container:

```powershell
docker compose up --build -d --force-recreate
```

## Important

Ollama's API does not gain user authentication from this client container. Anyone who can enter the helper container can use the configured Ollama API. Keep Docker access limited to trusted users, and avoid publishing the Ollama API to untrusted networks. The model must already be available to the Ollama server.
