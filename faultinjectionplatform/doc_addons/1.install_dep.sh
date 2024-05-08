#!/bin/bash

# 设置脚本在遇到错误时退出，并捕捉信号执行清理操作
set -e
trap cleanup EXIT

# 定义清理操作函数
cleanup() {
  echo "清理本地仓库和临时文件..."
  rm -rf /etc/apt/keyrings/docker.gpg
  rm -f kubectl minikube-linux-amd64 minikube helm
}

# 定义软件的版本号变量
# 在华为部署时 Docker 的版本号应该要修改
DOCKER_VERSION="5:20.10.15~3-0~ubuntu-focal"
KUBECTL_VERSION="v1.22.2"
MINIKUBE_VERSION="v1.23.2"
HELM_VERSION="v3.10.0"

# 安装Docker Engine
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
# 使用 yum 进行安装
# sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# sudo yum install docker-ce=20.10.15
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# echo \
#   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# sudo apt-get update
# sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# # 锁定Docker Engine的版本，防止被自动更新
# sudo apt-mark hold docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 安装kubectl
# 使用yum 进行安装
# sudo yum install -y kubectl
curl -LO "https://dl.k8s.io/release/$KUBECTL_VERSION/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client --output=yaml

# 安装minikube 
curl -LO https://storage.googleapis.com/minikube/releases/$MINIKUBE_VERSION/minikube-linux-amd64
install minikube-linux-amd64 /usr/local/bin/minikube
minikube version

# 安装helm charts 
# 使用 yum 安装 snapd
# sudo yum install epel-release
# sudo yum install snapd
# sudo systemctl enable --now snapd.socket
# sudo ln -s /var/lib/snapd/snap /snap
sudo apt install snapd

# echo https://mirrors.huaweicloud.com/helm/$HELM_VERSION/helm-$HELM_VERSION-linux-amd64.tar.gz
# # curl -LO https://mirrors.huaweicloud.com/helm/$HELM_VERSION/helm-$HELM_VERSION-linux-amd64.tar.gz
# curl -LO https://storage.googleapis.com/minikube/releases/$HELM_VERSION/minikube-linux-amd64
# install helm-$HELM_VERSION-linux-amd64.tar.gz /usr/local/bin/helm

sudo snap install helm --classic
# 如果通过snap安装不成功，则可执行这条指令：
# curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
# 安装其他工具:
# 使用 yum 安装其他工具
sudo apt install make
