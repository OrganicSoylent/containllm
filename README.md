# Deepseek in Minikube (local computer)
[Link to guide](https://www.linkedin.com/pulse/deepseek-kubernetes-ai-powered-reasoning-scale-brains-upgrade-i56pc)

To start the Minikube cluster with GPU usage, run:
```
minikube start --driver docker --container-runtime docker --gpus all --insecure-registry="localhost:5000"

minikube start --driver docker --container-runtime docker --gpus all --insecure-registry="192.168.49.2:5000"
```
Enable a image registry on minikube:
```
minikube addons enable registry

kubectl get svc -n kube-system | grep registry

minikube ip
```
re-tag docker image of crewai to be pushed into local minikube registry
```
docker tag crewai:latest 192.168.49.2:5000/crewai:latest
docker push 192.168.49.2:5000/crewai:latest
```
To enable access to apps on the cluster, run this in a second terminal (and keep it running):
```
minikube tunnel
```
To make a model available in the openweb-ui, you have to pull it in the ollama-pod first:
```
kubectl exec pod/<ollama-pod> -- ollama pull deepseek-r1:1.5b
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
add it to the docker daemon config and check again
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

# Kubernetes Dashboard

### Install the dashboard using Helm

Add kubernetes-dashboard repository
```
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```
Deploy a Helm Release named "kubernetes-dashboard" using the kubernetes-dashboard chart
```
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```
The service to access the UI is "kubernetes-dashboard-kong-proxy" and is set to ClusterIP by default.
Change it to LoadBalancer:
```
kubectl patch svc kubernetes-dashboard-kong-proxy -p '{"spec": {"type": "LoadBalancer"}}' -n kubernetes-dashboard
```

Ensure the cluster is tunneling. Probably you will have to type in your sudo password in the tunneling terminal to give access to the LoadBalancer. 

The Login should be accessible on [127.0.0.1:443](https://127.0.0.1:443)

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

# Run CrewAI locally (Optional)
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

# Deplyoing Deepseek-R1 in container

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

# Install Minikube
[Link to guide](https://www.virtualizationhowto.com/2021/11/install-minikube-in-wsl-2-with-kubectl-and-helm/)

1. Install Docker in WSL 2
2. Install Minikube prerequisites
3. Install Minikube
4. Install kubectl and set context to Minikube
5. Install Helm
6. Start the Minikube Kubernetes cluster

## 1. Install Docker in WSL 2
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

## 2. Install Minikube prerequisites
Install Conntrack
```
sudo apt install -y conntrack
```

## 3. Install Minikube
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

## 4. Install kubectl and set context to Minikube
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

## 5. Install Helm
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

chmod 700 get_helm.sh

./get_helm.sh
```
