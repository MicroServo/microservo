# 最好不要整个脚本一起执行, proxy_ip需要修改为自己的代理IP
export proxy_ip=10.22.59.177
export http_proxy=http://$proxy_ip:7890
export https_proxy=http://$proxy_ip:7890
export HTTP_PROXY=http://$proxy_ip:7890
export HTTPS_PROXY=http://$proxy_ip:7890
export no_proxy=localhost,127.0.0.1,10.96.0.0/12,192.168.0.1/16,192.168.49.2
export NO_PROXY=localhost,127.0.0.1,10.96.0.0/12,192.168.0.1/16,192.168.49.2

if  [ ! -d ~/.docker ] ; then
    mkdir ~/.docker
fi

minikube start --image-mirror-country=cn --registry-mirror https://docker.mirrors.ustc.edu.cn --docker-env http_proxy $http_proxy --docker-env https_proxy $https_proxy --docker-env no_proxy $no_proxy --cpus=32 --memory 64768 --disk-size 1024g

minikube start --docker-env http_proxy $http_proxy --docker-env https_proxy $https_proxy --docker-env no_proxy $no_proxy --cpus=32 --memory 64768 --disk-size 1024g
