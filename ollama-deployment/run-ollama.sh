#!/bin/bash

echo "Starting Ollama server..."
ollama serve &

# Wait for Ollama server to be up and running
echo "Waiting for Ollama server to be active..."
until curl --silent --fail http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done

echo "Ollama server is ready. Pulling model..."
ollama pull deepseek-r1:1.5b
