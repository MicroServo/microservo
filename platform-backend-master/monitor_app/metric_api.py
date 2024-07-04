import os
import random
from datetime import datetime
from typing import Union

import pandas as pd
import pytz
from prometheus_api_client import PrometheusConnect

from . import pod_list, monitor_config, service_list

normal_metrics = [
    # author psy7604
    # 根据筛选的指标构建需要的指标集合
    # cpu
    "container_cpu_usage_seconds_total",
    "container_cpu_user_seconds_total",
    "container_cpu_system_seconds_total",
    "container_cpu_cfs_throttled_seconds_total",
    "container_cpu_cfs_throttled_periods_total",
    "container_cpu_cfs_periods_total",
    "container_cpu_load_average_10s",
    # memory
    "container_memory_cache",
    "container_memory_usage_bytes",
    "container_memory_working_set_bytes",
    "container_memory_rss",
    "container_memory_mapped_file",
    # spec
    "container_spec_cpu_period",
    "container_spec_cpu_quota",
    "container_spec_memory_limit_bytes",
    "container_spec_cpu_shares",
    # threads
    "container_threads",
    "container_threads_max"
    # network
    "container_network_receive_errors_total",
    "container_network_receive_packets_dropped_total",
    "container_network_receive_packets_total",
    "container_network_receive_bytes_total",
    "container_network_transmit_bytes_total",
    "container_network_transmit_errors_total",
    "container_network_transmit_packets_dropped_total",
    "container_network_transmit_packets_total"
]
istio_metrics = [
    # istio
    "istio_requests_total",
    "istio_request_duration_milliseconds_sum",
    "istio_request_bytes_sum",
    "istio_response_bytes_sum",
    "istio_request_messages_total",
    "istio_response_messages_total",
    "istio_tcp_sent_bytes_total",
    "istio_tcp_received_bytes_total",
    "istio_tcp_connections_opened_total",
    "istio_tcp_connections_closed_total"
]
network_metrics = [
    # network
    "container_network_receive_errors_total",
    "container_network_receive_packets_dropped_total",
    "container_network_receive_packets_total",
    "container_network_receive_bytes_total",
    "container_network_transmit_bytes_total",
    "container_network_transmit_errors_total",
    "container_network_transmit_packets_dropped_total",
    "container_network_transmit_packets_total"
]

def time_format_transform(time):
    # 将int型time数据转换成date型
    if isinstance(time, int):
        time = datetime.fromtimestamp(time)
    # postman测试用例需要，发的是str型
    if isinstance(time, str):
        time = int(time)
        time = datetime.fromtimestamp(time)
    return time


def istio_cmdb_id_format(metric):
    pod = metric['pod']
    service = pod.split('-')[0]
    source_service = metric['source_canonical_service']
    destination_service = metric['destination_canonical_service']

    if source_service not in service_list and source_service != 'unknown':
        return ''
    if destination_service not in service_list and source_service != 'unknown':
        return ''

    if service == source_service:
        cmdb_id = '.'.join([pod, 'source', source_service, destination_service])
    else:
        cmdb_id = '.'.join([pod, 'destination', source_service, destination_service])
    return cmdb_id

def network_kpi_name_format(metric):
    kpi_name = metric['__name__']

    if 'interface' in metric:
        kpi_name = '.'.join([kpi_name, metric['interface']])

    return kpi_name

def istio_kpi_name_format(metric):
    kpi_name = metric['__name__']
    if 'request_protocol' in metric:
        protocol = metric['request_protocol']
        response_code = ''
        if 'response_code' in metric:
            response_code = metric['response_code']

        grpc_response_status = ''
        if 'grpc_response_status' in metric:
            grpc_response_status = metric['grpc_response_status']

        if protocol == 'tcp':
            response_flag = metric['response_flags']
            kpi_name = '.'.join([kpi_name, response_flag])
        else:
            kpi_name = '.'.join([kpi_name, protocol, response_code, grpc_response_status])
    return kpi_name


class PrometheusAPI:
    # disable_ssl –（bool）如果设置为 True，将禁用对向 prometheus 主机发出的 http 请求的 SSL 证书验证
    def __init__(self, url: str):
        self.client = PrometheusConnect(url, disable_ssl=True)

    # start_time: Union[int, datetime]表示变量既可以是int型也可以是datetime型
    def query_range(self, metric_name: str, pod: str, start_time: Union[int, datetime, str],
                    end_time: Union[int, datetime, str], namespace: str = 'default', step: int = 60):
        start_time = time_format_transform(start_time)
        end_time = time_format_transform(end_time)
        interface = 'eth0'
        if metric_name.endswith("_total") or metric_name in ['container_last_seen', 'container_memory_cache', 'container_memory_max_usage_bytes']:
            if metric_name in network_metrics:
                query = f"irate({metric_name}{{pod='{pod}', interface='{interface}'}}[5m])"
            # 拼接prometheus 查询语句
            else:
                query = f"rate({metric_name}{{pod=~'{pod}', namespace='{namespace}'}}[5m])"
        else:
            query = f"{metric_name}{{pod=~'{pod}', namespace='{namespace}'}}"
        data_raw = self.client.custom_query_range(query, start_time, end_time, step=step)

        if len(data_raw) == 0:
            return {"error": f"No data found for metric {metric_name} and pod {pod}"}
        else:
            data = []
            for item in data_raw[0]['values']:
                date_time = datetime.fromtimestamp(int(item[0]))
                date_time = date_time.astimezone(pytz.timezone('Asia/Shanghai'))
                float_value = round(float(item[1]), 3)  # float value is needed to be able to add it to the list as a whole.
                data.append({'time': date_time, 'value': float_value})
            return data

    # 用于算法获取metric数据
    def export_all_metrics(self, start_time, end_time, save_path, step=15):
        print('export_all_metrics')
        save_path = os.path.join(save_path, 'metric')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        namespace = monitor_config['namespace']
        # 采集container指标
        container_save_path = os.path.join(save_path, 'container')
        os.makedirs(container_save_path)
        # 采集istio指标
        istio_save_path = os.path.join(save_path, 'istio')
        os.makedirs(istio_save_path)

        interval_time = 2 * 60 * 60
        while start_time < end_time:
            if start_time + interval_time > end_time:
                current_et = end_time
            else:
                current_et = start_time + interval_time
            for metric in normal_metrics:
                data_raw = self.client.custom_query_range(f"{metric}{{namespace='{namespace}'}}", time_format_transform(start_time), time_format_transform(current_et), step=step)
                if len(data_raw) == 0:
                    continue
                timestamp_list = []
                cmdb_id_list = []
                kpi_list = []
                value_list = []
                for data in data_raw:
                    if data['metric']['pod'] not in pod_list:
                        continue
                    cmdb_id = data['metric']['instance'] + '.' + data['metric']['pod']
                    if cmdb_id == '':
                        continue
                    kpi_name = metric
                    if metric in network_metrics:
                        kpi_name = network_kpi_name_format(data['metric'])
                    for d in data['values']:
                        timestamp_list.append(int(d[0]))
                        cmdb_id_list.append(cmdb_id)
                        kpi_list.append(kpi_name)
                        value_list.append(round(float(d[1]), 3))
                dt = pd.DataFrame({
                    'timestamp': timestamp_list,
                    'cmdb_id': cmdb_id_list,
                    'kpi_name': kpi_list,
                    'value': value_list
                })
                dt = dt.sort_values(by='timestamp')
                file_path = os.path.join(container_save_path, 'kpi_'+metric+'.csv')
                if os.path.exists(file_path):
                    # 文件存在，追加数据
                    with open(file_path, 'a', encoding='utf-8', newline='') as f:
                        dt.to_csv(f, header=False, index=False)
                else:
                    # 文件不存在，写入新文件
                    dt.to_csv(file_path, index=False)
            
            for metric in istio_metrics:
                data_raw = self.client.custom_query_range(f"{metric}{{namespace='{namespace}'}}", time_format_transform(start_time), time_format_transform(current_et), step=step)
                if len(data_raw) == 0:
                    continue
                timestamp_list = []
                cmdb_id_list = []
                kpi_list = []
                value_list = []
                for data in data_raw:
                    cmdb_id = istio_cmdb_id_format(data['metric'])
                    pod_name = cmdb_id.split('.')[0]
                    if cmdb_id == '' or pod_name not in pod_list:
                        continue
                    kpi_name = istio_kpi_name_format(data['metric'])
                    for d in data['values']:
                        timestamp_list.append(int(d[0]))
                        cmdb_id_list.append(cmdb_id)
                        kpi_list.append(kpi_name)
                        value_list.append(round(float(d[1]), 3))
                dt = pd.DataFrame({
                    'timestamp': timestamp_list,
                    'cmdb_id': cmdb_id_list,
                    'kpi_name': kpi_list,
                    'value': value_list
                })
                dt = dt.sort_values(by='timestamp')
                file_path = os.path.join(istio_save_path, 'kpi_'+metric+'.csv')
                if os.path.exists(file_path):
                    # 文件存在，追加数据
                    with open(file_path, 'a', encoding='utf-8', newline='') as f:
                        dt.to_csv(f, header=False, index=False)
                else:
                    # 文件不存在，写入新文件
                    dt.to_csv(file_path, index=False)
            start_time = current_et
    
    def get_all_metrics(self):
        '''获取所有的metrics'''
        # 调用prometheus的all_metrics方法获取所有的名称列表
        all_metrics = self.client.all_metrics()
        all_metrics = list(filter(lambda x: True if x in normal_metrics else False, all_metrics))
        return all_metrics
