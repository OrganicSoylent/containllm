# Deepseek in Minikube (local computer)
[Link to guide](https://www.linkedin.com/pulse/deepseek-kubernetes-ai-powered-reasoning-scale-brains-upgrade-i56pc)


## Install Minikube
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

Print the admin access-token related to the serviceaccount created in the deployment
```
kubectl -n kube-system create token k8sadmin
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
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
```
