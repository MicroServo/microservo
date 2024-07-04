import pathlib
import sys

from kubernetes import config, client
from yaml import full_load

root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)
# 读取配置文件
monitor_config = full_load(open(root_path / "monitor_config.yaml", "r"))
root_config = full_load(open(root_path / "config.yaml", "r"))
def get_pod_list(v1, namespace='default'):
    pod_list = v1.list_namespaced_pod(namespace)
    pod_names = []
    # 遍历获取到的Pods,把名称存储到列表中
    for pod in pod_list.items:
        pod_names.append(pod.metadata.name)
    return pod_names

def get_services_list(v1, namespace='default'):
    # 获取指定命名空间下的所有服务
    service_list = v1.list_namespaced_service(namespace)

    # 初始化一个列表来存储服务的名称
    services_names = []

    # 遍历获取到的服务，把名称存储到列表中
    for service in service_list.items:
        services_names.append(service.metadata.name)

    return services_names

config.kube_config.load_kube_config(config_file=root_config['kubernetes_path'])
v1 = client.CoreV1Api()
pod_list = [pod for pod in get_pod_list(v1, namespace=monitor_config['namespace']) if not pod.startswith('loadgenerator-') and not pod.startswith('redis-cart')]

service_list = get_services_list(v1, namespace=monitor_config['namespace'])

from monitor_app.metric_api import PrometheusAPI
from monitor_app.trace_api import TraceAPI
from monitor_app.log_api import logAPI
# 实例化PrometheusAPI类对象并查询数据
prom = PrometheusAPI(monitor_config["prometheusApi"])
# 实例化traceAPI类对象并查询数据
trace = TraceAPI(monitor_config['api'], monitor_config['username'], monitor_config['password'])
# 实例化logAPI类对象并查询数据
log = logAPI(monitor_config['api'], monitor_config['username'], monitor_config['password'])
