#!/bin/bash

if  [ ! -d ~/.docker ] ; then
    mkdir ~/.docker
fi

if [ -f ~/.docker/config.json ]; then
    cp ~/.docker/config.json ~/.docker/config.json.bak
fi

if minikube status | grep -q 'Running'; then
    minikube stop
fi

minikube start --image-mirror-country=cn --registry-mirror https://docker.mirrors.ustc.edu.cn --kubernetes-version=v1.26.3  --cpus=32 --memory 64768 --disk-size 150g