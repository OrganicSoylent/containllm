# Run CrewAI & Deepseek-R1 in a local Minikube Cluster

## Table of contents
__I. Cluster Quickstart__
1. [Enable Nvidia runtime in Docker](#1-enable-nvidia-runtime-in-docker)
2. [Start the Cluster](#2-start-the-cluster)
3. [Enable image registry](#3-enable-image-registry)
4. [Enable outside access to cluster](#4-enable-outside-access-to-cluster)

__II. Applications Quickstart__
1. [Create Namespaces](#1-create-namespaces)
2. [Kubernetes Dashboard](#2-kubernetes-dashboard)
3. [Ollama & Openweb-UI](#3-ollama--openweb-ui)
4. [CrewAI](#4-crewai)

## I. Cluster Quickstart
Requires all [prerequesits]() first.

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
Starts Minikube cluster with GPU usage and an internal image registry enabled
```
minikube start --driver docker --container-runtime docker --gpus all --addons=registry --insecure-registry="192.168.49.2:5000"
```
_Note: The IP address of the registry needs to be set in the docker daemon.json first ([reference](#configure-docker-daemon))_

### 3. Enable image registry
This is required to use prebuilt images for crewai and ollama. Requires building images from Dockerfile first ([reference]())
```
minikube addons enable registry

# check if registry is deployed
kubectl get svc -n kube-system | grep registry

# optional: check if IP address is the same as in docker daemon.json
minikube ip
```

### 4. Enable outside access to cluster
To enable access to apps on the cluster, run this in a second terminal __and keep it running__:
```
minikube tunnel
```
_Note: When deploying a LoadBalancer to the cluster, you will have to provide your sudo password in this terminal once, to unblock the tunnel._

## II. Applications Quickstart
### 1. Create Namespaces
```
kubectl apply -f namespace.yaml
```
### 2. Kubernetes Dashboard
__Only first time necessary:__ Add kubernetes-dashboard repository to Helm
```
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```
Deploy kubernetes-dashboard chart to the cluster
```
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```
Install the cluster-admin serviceaccount and role
```
kubectl apply -f ./kubernetes-dashboard/.
```
The service to access the UI is "kubernetes-dashboard-kong-proxy" and is set to ClusterIP by default.
Change it to LoadBalancer:
```
kubectl patch svc kubernetes-dashboard-kong-proxy -p '{"spec": {"type": "LoadBalancer"}}' -n kubernetes-dashboard
```
Ensure the [cluster is tunneling and the tunnel is unlocked](#4-enable-outside-access-to-cluster). 

The Login should be accessible on [127.0.0.1:443](https://127.0.0.1:443)

__The Browser might warn you for accessing an insecure connection. Ignore this and access it through the "advanced" Option__

Print the admin access-token related to the serviceaccount created by _manifests
```
kubectl -n kubernetes-dashboard create token k8sadmin
```
Change the annoying time-to-logout in the kubernetes-dashboard-kong deployment (edit through dashboard or kubectl edit). You can find the setting as:
```
- name: kubernetes-dashboard-kong-token
  projected:
    defaultMode: 420
    sources:
      - serviceAccountToken:
          expirationSeconds: <change this value>
```

### 3. Ollama & Openweb-UI
Deploys the Ollama & Openweb-UI Pods in the "ollama"-namespace.
```
kubectl apply -f ./llm-deployment/.
```
Check deployment progress
```
kubectl get pods -n ollama
kubectl get svc -n ollama
```
__Will be deprecated after container image is ready__
To make a model available in the openweb-ui, you have to pull it in the ollama-pod first. Deploys the smallest available deepseek model:
```
kubectl exec pod/<ollama-pod> -- ollama pull deepseek-r1:1.5b
```
_Note: you can also to this through the Kubernetes dashboard._

### 4. CrewAI
Push the docker image to the registry in the cluster
```
docker push 192.168.49.2:5000/crewai:latest
```
Apply the deployment
```
kubectl apply -f ./crewcontainer/.
```

### Troubleshooting nvidia-container-runtime
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
#### configure docker daemon
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

## Run CrewAI locally (Optional)
Useful for creating a basic project template.

Install crewai in a virtual environment (Python > 3.11 required). 
1. Create a virtual Python environment
```
python3.12 -m venv crewai-env
source crewai-env/bin/activate
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

## Deplyoing Deepseek-R1 in container
Steps
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

## III. Prerequesits
__Minikube__
1. [Install Docker in WSL 2]()
2. [Install Minikube prerequisites]()
3. [Install Minikube]()
4. [Install kubectl and set context to Minikube]()
5. [Install Helm]()
6. [Start the Minikube Kubernetes cluster]()

__Build docker images__
1. [Build the CrewAI Image](#1-build-the-crewai-image)
2. [Build-the-Ollama-Image](#1-build-the-ollama-image)

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

## Build docker images
### 1. Build the CrewAI Image
```
docker build -t crewai:latest ./crewcontainer/.
```
re-tag docker image of crewai to be pushed into local minikube registry
```
docker tag crewai:latest 192.168.49.2:5000/crewai:latest
```
### 1. Build the Ollama Image
__TBD__

# Sources
- [Blogpost for running Deepseek in Kubernetes](https://www.linkedin.com/pulse/deepseek-kubernetes-ai-powered-reasoning-scale-brains-upgrade-i56pc)

- [Guide for installing Minikube](https://www.virtualizationhowto.com/2021/11/install-minikube-in-wsl-2-with-kubectl-and-helm/)