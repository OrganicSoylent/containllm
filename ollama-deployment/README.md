# Ollama server guide

## Ollama commands from outside the container
```
kubectl get pods -n ollama

kubectl exec -n ollama <ollama-pod-name> -it -- /bin/sh
```

## Ollama commands
```
ollama list

ollama ps

ollama pull <model-name>:<parameter-version> # e.g. deepseek-r1:1.5b

ollama run <model-name>:<parameter-version> # e.g. deepseek-r1:1.5b

ollama stop <model-name>:<parameter-version> # e.g. deepseek-r1:1.5b
```

## Ollama configuration parameters

