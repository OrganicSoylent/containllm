# Deplyoing Deepseek-R1 in container

Steps
1. Install Ollama cli
```
curl -fsSL https://ollama.com/install.sh | sh
```

2. Pull Deepseek-R1 model from registry (using the default 7 billion parameters model)
```
ollama pull deepseek-r1:7b
```