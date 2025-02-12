#!/bin/sh
ollama serve &  # Start Ollama in the background
sleep 2         # Wait for it to initialize
ollama pull deepseek-r1:7b  # Pull Llama 3 model
tail -f /dev/null  # Keep the container running