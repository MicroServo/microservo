#!/bin/bash

# 检查是否存在~/.docker目录，如果不存在则创建一个
if  [ ! -d ~/.docker ] ; then
    mkdir ~/.docker
fi

# 检查是否存在~/.docker/config.json文件，如果存在则备份一个副本
if [ -f ~/.docker/config.json ]; then
    cp ~/.docker/config.json ~/.docker/config.json.bak
fi

# 检查是否已经启动了minikube集群，如果已经启动则停止它
if minikube status | grep -q 'Running'; then
    minikube stop
fi

# 启动minikube集群，并指定使用环境变量中的代理设置和其他参数
# profile参数：创建的docker镜像的名字，默认是minikube
# 如果有两个用户同时运行且使用相同profile名，则会使用同一个镜像
minikube start --profile your_profile_name --image-mirror-country=cn --registry-mirror https://docker.mirrors.ustc.edu.cn --kubernetes-version=v1.26.3  --cpus=32 --memory 64768 --disk-size 1024g