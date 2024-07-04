#!/bin/bash

set -e
trap cleanup EXIT

cleanup() {
  echo "清理本地仓库和临时文件..."
  rm -rf /etc/apt/keyrings/docker.gpg
  rm -f kubectl minikube-linux-amd64 minikube helm
}

DOCKER_VERSION="5:20.10.15~3-0~ubuntu-focal"
KUBECTL_VERSION="v1.22.2"
MINIKUBE_VERSION="v1.23.2"
HELM_VERSION="v3.10.0"

# Docker Engine
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin


curl -LO "https://dl.k8s.io/release/$KUBECTL_VERSION/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client --output=yaml

# minikube 
curl -LO https://storage.googleapis.com/minikube/releases/$MINIKUBE_VERSION/minikube-linux-amd64
install minikube-linux-amd64 /usr/local/bin/minikube
minikube version

# helm
sudo apt install snapd

sudo snap install helm --classic

sudo apt install make
