#!/usr/bin/env python3
"""Minimal interactive terminal client for an Ollama chat API."""

import json
import os
import sys
import urllib.error
import urllib.request


BASE_URL = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:0.6b")


def chat(messages):
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": True}).encode()
    request = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            answer = []
            for line in response:
                if not line.strip():
                    continue
                item = json.loads(line)
                piece = item.get("message", {}).get("content", "")
                if piece:
                    print(piece, end="", flush=True)
                    answer.append(piece)
            print()
            return "".join(answer)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"Ollama returned HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(
            f"Cannot reach Ollama at {BASE_URL}. Check OLLAMA_URL and that Ollama is running. ({exc})"
        ) from exc


def main():
    print(f"Ollama terminal chat — model: {MODEL}")
    print(f"API: {BASE_URL}")
    print("Type /reset to clear the conversation, /exit to quit.\n")
    messages = []
    while True:
        try:
            prompt = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return
        if not prompt:
            continue
        if prompt.lower() in {"/exit", "/quit"}:
            return
        if prompt.lower() == "/reset":
            messages.clear()
            print("Conversation cleared.\n")
            continue
        messages.append({"role": "user", "content": prompt})
        print("assistant> ", end="", flush=True)
        try:
            answer = chat(messages)
            messages.append({"role": "assistant", "content": answer})
        except RuntimeError as exc:
            messages.pop()
            print(f"\nError: {exc}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
