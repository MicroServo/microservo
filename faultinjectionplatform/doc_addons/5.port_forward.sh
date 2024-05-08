#!/bin/bash
# 这是一个端口转发的脚本，可以转发prometheus，elasticsearch，kibana，grafana四个服务的端口
# 你可以根据你的实际情况修改服务名和端口号

# 定义一个函数，用来检查本地端口是否被占用，如果是，就退出脚本
check_port() {
  local_port=$1
  netstat -ntlp | grep $local_port > /dev/null
  if [ $? -eq 0 ]; then
    echo "Local port $local_port is already in use, please change another one."
    exit 1
  fi
}

# 定义一个函数，用来杀掉已经运行的端口转发进程，然后重新启动一个新的端口转发进程，并将输出重定向到一个日志文件
port_forward() {
  service_name=$1
  local_port=$2
  remote_port=$3
  log_file=$4
  pid=$(ps -aux|grep -w "kubectl port-forward svc/$service_name -n observe --address 0.0.0.0 $local_port:$remote_port"|grep -v 'grep'|awk '{print $2}');
  if [ -n "$pid" ] ; then
    echo "Found process:" $pid
    kill -9 $pid
  fi
  nohup kubectl port-forward svc/$service_name -n observe --address 0.0.0.0 $local_port:$remote_port > $log_file &
}

# 转发prometheus的端口，本地端口为9090，远程端口为9090，日志文件为prometheus.log
check_port 9090
port_forward prometheus 9090 9090 prometheus.log

# 转发elasticsearch的端口，本地端口为9200，远程端口为9200，日志文件为elasticsearch.log
check_port 9200
port_forward elasticsearch 9200 9200 elasticsearch.log

# 转发kibana的端口，本地端口为5601，远程端口为5601，日志文件为kibana.log
check_port 5601
port_forward kibana 5601 5601 kibana.log

# 转发grafana的端口，本地端口为3000，远程端口为3000，日志文件为grafana.log
check_port 3000
port_forward grafana 3000 3000 grafana.log
