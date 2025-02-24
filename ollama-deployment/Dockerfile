# # Use a base image with CUDA support if using GPU, otherwise use Ubuntu
FROM ubuntu:22.04

# # Set non-interactive mode to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# # Install required dependencies
RUN apt update && apt install -y \
    curl \
    git \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# # Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh
# FROM ollama/ollama

COPY ./run-ollama.sh /tmp/run-ollama.sh

WORKDIR /tmp

RUN chmod +x run-ollama.sh \
    && ./run-ollama.sh

# Expose Ollama's default port (if needed)
EXPOSE 11434