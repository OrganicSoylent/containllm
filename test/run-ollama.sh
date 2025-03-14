#!/bin/bash

echo "Starting Ollama server in the background..."
ollama serve &

echo "Waiting for Ollama server to be active..."
while ! ollama list >/dev/null 2>&1; do
  sleep 1
done

echo "Ollama server is running. Pulling model..."
ollama pull "$MODEL_NAME"

echo "Stopping Ollama server..."
pkill -f "ollama serve"

echo "Model download complete."
