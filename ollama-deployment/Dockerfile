FROM ollama/ollama

COPY ./run-ollama.sh /tmp/run-ollama.sh

WORKDIR /tmp

RUN chmod +x run-ollama.sh \
    && ./run-ollama.sh

# Expose Ollama's default port (if needed)
EXPOSE 11434
CMD ["ollama", "pull deepseek-r1:1.5b"]