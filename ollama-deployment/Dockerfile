FROM ubuntu:22.04 AS final

# Set non-interactive mode to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Define the model storage path
ENV OLLAMA_MODELS=/models

# Install required dependencies
RUN apt update && apt install -y \
    curl \
    git \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the downloaded models into Ollama's model directory
COPY models/ $OLLAMA_MODELS/

# Expose Ollama's default port (if needed)
EXPOSE 11434

CMD ["ollama", "serve"]
