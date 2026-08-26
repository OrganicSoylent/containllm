# Run CrewAI & Deepseek-R1 in a local Minikube Cluster
Deploy locally in a Kubernetes managed environement
- Ollama server for running any LLM
- OpenWebUI
- n8n AI agent framework
- Apache APISIX API Gateway

Optionally, you can leverage the advantages of Kubernetes through
- Kubernetes Dashboard lets you easily manage the Cluster
- ArgoCD for automated deployment of your changes (wip)


## 0. Cluster Quickstart
For initial setup, check the [prerequesits](#iv-prerequesits) first.

```
minikube config set driver podman
minikube config set container-runtime containerd
minikube config set rootless true

minikube config view
```

Starts Minikube cluster:
```
minikube start
```

To enable access to apps on the cluster, run this in a second terminal __and keep it running__:
```
minikube tunnel
```

# II. Prerequesits
This setup requires installation of
- Nvidia-Container-Toolkit (if you use a NVIDIA GPU)
- Podman
- Minikube & kubectl
- Helm

## II. Applications
List of externally accessible services

|service|namespace|address|
|---|---|---|
|openweb-ui-svc|openwebui|[127.0.0.1:9300](http://localhost:9300)|
|n8n-external|n8n|[127.0.0.1:9200](http://localhost:9200)|
|k8s-dashboard-kong-proxy|k8s-dash|[127.0.0.1:9100](http://localhost:9100)|

<br>
<details> 
  <summary>In case you haven't noticed</summary>
  <img src="./img/over_9000.jpg" alt="over 9000" width="200"></img>
</details>


### 1. Ollama

Deploys the kubernetes resources in the "ollama" namespace
```
kubectl apply -f ollama-deployment/.

# Check deployment progress
kubectl get pods -n ollama
```
To download and run a LLM, you will have to go through the [Ollama server guide](ollama-deployment/README.md)

### 2. OpenwebUI
Deploy Kubernetes resources
```
kubectl apply -f ./openwebui-deployment/.

# Check deployment progress
kubectl get pods -n openwebui
```
The UI is accessible at [http://localhost:9300](http://localhost:9300)

### 3. ApiSIX
```
helm repo add apisix https://apache.github.io/apisix-helm-chart && helm repo update && helm upgrade --install apisix apisix/apisix --create-namespace  --namespace apisix --set dashboard.enabled=true --set ingress-controller.enabled=true --set ingress-controller.config.apisix.serviceNamespace=apisix
```

### 4. n8n AI-agent framework
Deploy the n8n AI agent framework in the "n8n" namespace
```
kubectl apply -f ./n8n-deployment/.

# Check deployment progress
kubectl get pods -n n8n
```
The UI is accessible at [http://localhost:9200](http://localhost:9200)

### 5. Kubernetes Dashboard
The repo contains a customized version of the [Kubernetes Dashboard](#3-kubernetes-dashboard-customization).

__Ensure the [cluster is tunneling and the tunnel is unlocked](#4-enable-outside-access-to-cluster).__
```
kubectl apply -f ./kubernetes-dashboard/.
```
Check for deployment status
```
kubectl get pods -n k8s-dash
```
The Login should be accessible on [127.0.0.1:9100](https://127.0.0.1:9100)

__The Browser might warn you for accessing an insecure connection. Ignore this and access it through the "advanced" option__

Print the admin access-token related to the serviceaccount created by _manifests
```
kubectl -n k8s-dash create token k8sadmin
```

### 6. ArgoCD
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
```
kubectl patch svc argocd-server -n argocd --type='json' -p='[
  {"op": "replace", "path": "/spec/type", "value": "LoadBalancer"},
  {"op": "replace", "path": "/spec/ports/1/port", "value": 9000}
]'
```
The initial password for the admin account is auto-generated and stored as clear text in the field password in a secret named argocd-initial-admin-secret.
```
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data}'
```
Login with username _admin_ and the secret. In the options, connect the repo using ssh:
"git@github.com:OrganicSoylent/containllm.git"
```
cat ~/.ssh/id_ed25519
```
connect the application GUIDE HERE


## VI. Development
### 1. Run CrewAI locally (Optional)
Useful for creating a basic project template.

Install crewai in a virtual environment (Python > 3.11 required).
```
cd crewai-deployment/crew_setup/src/stock_crew/

python3.12 -m venv env

source env/bin/activate
```
Install Crewai library
```
pip install crewai
```
Create a CrewAI project template
```
crewai create crew <crew-name>
```
Exit virtual environment
```
deactivate
```

### 2. Deply Deepseek in single container
Development of Dockerfile
1. Install Ollama cli
```
curl -fsSL https://ollama.com/install.sh | sh
```
2. Pull Deepseek-R1 model from registry (using the default 7 billion parameters model)
```
ollama pull deepseek-r1:1.5b
```
3. NVIDIA nvidia-container-toolkit is required
```
dpkg -l | grep nvidia-container-toolkit
```
If it is not installed, run
```
distribution=$(. /etc/os-release;echo $ID $VERSION_ID)

curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -

curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list

sudo apt update

sudo apt install -y nvidia-container-toolkit
```

### 3. Kubernetes Dashboard customization
Add kubernetes-dashboard repository to Helm
```
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```
Deploy kubernetes-dashboard chart to the cluster
```
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --namespace kubernetes-dashboard
```

The service to access the UI is "kubernetes-dashboard-kong-proxy" and is set to ClusterIP by default.
Change it to LoadBalancer:
```
kubectl patch svc kubernetes-dashboard-kong-proxy -p '{"spec": {"type": "LoadBalancer"}}' -n kubernetes-dashboard
```


# Sources
- [Blogpost for running Deepseek in Kubernetes](https://www.linkedin.com/pulse/deepseek-kubernetes-ai-powered-reasoning-scale-brains-upgrade-i56pc)

- [Guide for installing Minikube](https://www.virtualizationhowto.com/2021/11/install-minikube-in-wsl-2-with-kubectl-and-helm/)


