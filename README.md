# Run CrewAI & Deepseek-R1 in a local Minikube Cluster

## Table of contents
__I. Cluster Quickstart__
1. [Enable Nvidia runtime in Docker](#1-enable-nvidia-runtime-in-docker)
2. [Start the Cluster](#2-start-the-cluster)
3. [Enable outside access to cluster](#3-enable-outside-access-to-cluster)

__II. Applications Quickstart__
1. [Ollama](#1-ollama)
2. [CrewAI](#2-crewai)
3. [OpenWebUI](#3-openwebui)

__III. Optional Tools__
1. [Kubernetes Dashboard](#1-kubernetes-dashboard)
2. [ArgoCD](#2-argocd)

__IV. Prerequesits__
1. [Install Docker in WSL 2](#1-install-docker-in-wsl-2)
2. [Install Minikube prerequisites](#2-install-minikube-prerequisites)
3. [Install Minikube](#3-install-minikube)
4. [Install kubectl and set context to Minikube](#4-install-kubectl-and-set-context-to-minikube)
5. [Install Helm](#5-install-helm)

__V. Troubleshooting__
1. [Troubleshooting nvidia-container-runtime](#1-troubleshooting-nvidia-container-runtime)
2. [Troubleshooting docker daemon](#2-troubleshooting-docker-daemon)

__[VI. Development](#vi-development)__

## I. Cluster Quickstart
For initial setup, check the [prerequesits](#iv-prerequesits) first.

### 1. Enable Nvidia runtime in Docker
Check if nvidia-container-runtime is already listed as docker runtime
```
docker info | grep -i runtime
```
If nvidia-runtime is not listed, restart docker and check again
```
sudo systemctl restart docker
```
If this doesn't work, go to the [troubleshooting section](#troubleshooting-nvidia-container-runtime).

### 2. Start the Cluster
Starts Minikube cluster with GPU usage.
```
minikube start --driver docker --container-runtime docker --gpus all
```
The same __without__ GPU usage.
```
minikube start --driver docker --container-runtime docker
```
### 3. Enable outside access to cluster
To enable access to apps on the cluster, run this in a second terminal __and keep it running__:
```
minikube tunnel
```
_Note: When deploying a LoadBalancer to the cluster, you will have to provide your sudo password in this terminal once, to unblock the tunnel._

## II. Applications Quickstart
### 1. Ollama

Deploys the kubernetes resources
```
kubectl apply -f ./ollama-deployment/.
```
Check deployment progress
```
kubectl get pods -n ollama
```
The ollama container comes with a preinstalled deepseek-r1 model (1.5b parameters).

### 2. CrewAI
The CrewAI deployment is conpletely scripted, so you can add required secrets and configurations in runtime. This is done to prevent any API-Key or other sensitive information to end up in the GitHub repo.

As of now, you need to provide this information:
- SERPER_API_KEY (for Serper webscraping)
- CAR_BRAND (for the marketing example)

Simply run this and follow the prompted instructions
```
sh crewai-deployment/deploy_crewai.sh
```


### 3. OpenwebUI
Deploy Kubernetes resources
```
kubectl apply -f ./openwebui-deployment/.
```
Check deployment progress
```
kubectl get pods -n openwebui
```
The UI should be accessible under [127.0.0.1:9000](http://127.0.0.1:9000)

## III. Optional Tools

### 1. Kubernetes Dashboard
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

### 2. ArgoCD
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

## IV. Prerequesits

### Minikube
#### 1. Install Docker in WSL 2
Install prerequisites
```
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```
Download and add the official Docker PGP key
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
Add the stable channel repository
```
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
Update the package list
```
sudo apt-get update -y
```
Install the latest Docker CE
```
sudo apt-get install -y docker-ce
```
Add your user to access the Docker CLI without root user permissions
```
sudo usermod -aG docker $USER && newgrp docker
```

#### 2. Install Minikube prerequisites
Install Conntrack
```
sudo apt install -y conntrack
```

#### 3. Install Minikube
```
# Download the latest Minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Make it executable
chmod +x ./minikube

# Move it to your user's executable PATH
sudo mv ./minikube /usr/local/bin/

#Set the driver version to Docker
minikube config set driver docker
```

#### 4. Install kubectl and set context to Minikube
```
# Download the latest Minikube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make it executable
chmod +x ./kubectl

# Move it to your user's executable PATH
sudo mv ./kubectl /usr/local/bin/

#set the context to Minikube
kubectl config use-context minikube
```

#### 5. Install Helm
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

chmod 700 get_helm.sh

./get_helm.sh
```

## V. Troubleshooting
### 1. Troubleshooting nvidia-container-runtime
Check if nvidia-container-runtime is already listed as docker runtime
```
docker info | grep -i runtime
```
If not, restart docker and check again
```
sudo systemctl restart docker
```
If it doesn't show _"Runtimes: io.containerd.runc.v2 nvidia runc"_, check that Docker is configured to use nvidia-container-runtime:
```
cat /etc/docker/daemon.json
```
If this doesn't include this
```
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

### 2. Troubleshooting docker daemon
```
sudo tee /etc/docker/daemon.json <<EOF
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "insecure-registries": ["192.168.49.2:5000"]
}
EOF
```
Sometimes, the nvidia-container-cli isn't properly linked after reboot. Try:
```
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

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