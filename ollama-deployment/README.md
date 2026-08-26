# Ollama server guide
The current setup requires manual download of a model from within an Ollama container. If a "pre-mounted model" setup might come in the future.

## Ollama commands from outside the container
Get inside an Ollama container/pod:
```
kubectl get pods -n ollama

kubectl exec -n ollama <ollama-pod-name> -it -- /bin/sh
```

## Ollama commands

Starting and stopping a model is __not required__, if you use OpenWebUI. Pulling/Downloading a model is __always required.__ __Check the model size before download, they can be very big!__

Here is a list of smaller models that can run locally on a consumer grade GPU (~16 GB vram)
|Model name|size params/GB |Ollama reference|
|---|---|---|
|Deepseek-r1|1.5b/1.1GB|deepseek-r1:1.5b|
|Deepseek-r1|7b/4.7GB|deepseek-r1:7b|
|Deepseek-r1|8b/5.2GB|deepseek-r1:8b|
|Deepseek-r1|14b/9.0GB|deepseek-r1:14b|
|codellama|7b/3.8GB|codellama:7b|
|codellama|13b/7.4GB|codellama:13b|

```
ollama list

ollama ps

ollama pull <model-name>:<parameter-version>

ollama run <model-name>:<parameter-version>

ollama stop <model-name>:<parameter-version>
```

>If you have started a model in the console it opens the chat with the model. If you want to exit the chat, type ``/bye``

## Ollama configuration parameters

Have been moved to the [configmap](1-configmap.yaml)
