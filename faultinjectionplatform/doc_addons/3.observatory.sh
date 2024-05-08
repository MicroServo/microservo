#!/bin/bash

# pull images (If download image during deploying, it chances that the progress will frequently fail)
# cache the images for a quicker retry
cd ../

if [ ! -f apm-server.tar ] ; then
    minikube image load docker.elastic.co/apm/apm-server:8.7.1
    minikube image save docker.elastic.co/apm/apm-server:8.7.1 apm-server.tar
else
    minikube image load apm-server.tar
fi

if [ ! -f elasticsearch.tar ] ; then
    minikube image load docker.elastic.co/elasticsearch/elasticsearch:8.7.1
    minikube image save docker.elastic.co/elasticsearch/elasticsearch:8.7.1 elasticsearch.tar
else
    minikube image load elasticsearch.tar
fi

if [ ! -f filebeat.tar ] ; then
    minikube image load docker.elastic.co/beats/filebeat:8.7.1
    minikube image save docker.elastic.co/beats/filebeat:8.7.1 filebeat.tar
else
    minikube image load filebeat.tar
fi

if [ ! -f kibana.tar ] ; then
    minikube image load docker.elastic.co/kibana/kibana:8.7.1
    minikube image save docker.elastic.co/kibana/kibana:8.7.1 kibana.tar
else
    minikube image load kibana.tar
fi

if [ ! -f logstash.tar ] ; then
    minikube image load docker.elastic.co/logstash/logstash:8.7.1
    minikube image save docker.elastic.co/logstash/logstash:8.7.1 logstash.tar
else
    minikube image load logstash.tar
fi

if [ ! -f metricbeat.tar ] ; then
    minikube image load docker.elastic.co/beats/metricbeat:8.7.1
    minikube image save docker.elastic.co/beats/metricbeat:8.7.1 metricbeat.tar
else
    minikube image load metricbeat.tar
fi

cd observe
kubectl create namespace observe

docker pull ghcr.io/chaos-mesh/chaos-daemon:v2.5.1
docker pull ghcr.io/chaos-mesh/chaos-dashboard:v2.5.1
docker pull ghcr.io/chaos-mesh/chaos-mesh:v2.5.1

# Chaos-mesh (for fault injection)
helm repo add chaos-mesh https://charts.chaos-mesh.org
kubectl create ns chaos-mesh
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --version=2.5.1 --set "dashboard.env.DATABASE_DRIVER=mysql" --set "dashboard.env.DATABASE_DATASOURCE=root:elastic@tcp(10.10.1.202:3306)/chaos_mesh?parseTime=true" --set "dashboard.securityMode=false" --set "dashboard.env.TTL_EVENT=336h" --set "dashboard.env.TZ=Asia/Shanghai"

# Elasticsearch (注意，必须要开启mnikube的这两个插件，否则无法成功运行elasticsearch)
minikube addons enable default-storageclass
minikube addons enable storage-provisioner
# ！下面这步是必须的：(因为ES的安装默认是分布式而非单机集群，因此需要修改)
cd elasticsearch/examples/minikube
helm install elasticsearch -n observe --values=values.yaml ../../
# get the users's password
kubectl get secrets --namespace=observe elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
# get the username (default: elastic)
kubectl get secrets --namespace=observe elasticsearch-master-credentials -o jsonpath="{.data.username}" | base64 -d
cd -

# Elastic APM server
# An cert issue in v8.4.2+ (https://github.com/elastic/apm-server/issues/10332)
# 进入apm-server, 执行 `apm-server test output` 可以校验是否成功
helm install apm-server ./apm-server -n observe

# Kibana (请务必等elasticsearch运行成功再进行后续操作)
# 可以先再另一个namespace创建kibana把镜像下载好，然后再在elastic namespace中安装
helm install kibana ./kibana -n observe

# 如果要使用logstash需要filebeat
helm install filebeat ./filebeat -n observe

# Logstash
sed -i 's/helm-logstash-elasticsearch/logstash/g' logstash/examples/elasticsearch/Makefile
sed -i 's/upgrade --wait/upgrade -n observe --wait/g' logstash/examples/elasticsearch/Makefile
cd logstash/examples/elasticsearch
helm install logstash -n observe --values=values.yaml ../../
cd -

# # prometheus
cd prometheus/charts
helm install prometheus -n observe ./prometheus
cd -

# # grafana
helm install grafana ./grafana -n observe
# # Get passwd: 
# # kubectl get secret --namespace observe grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

cd ..
