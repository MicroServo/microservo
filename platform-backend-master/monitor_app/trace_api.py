import os
import random
import time
from datetime import datetime
from datetime import timedelta
from typing import Union

import pandas as pd
import pytz
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout

from .utils.extract import merge_csv
from . import root_config, monitor_config
from ssl import create_default_context


def timezone_adjust(local_datetime):
    utc_time = local_datetime.astimezone(pytz.utc)
    # 格式化为 ISO 8601 格式字符串
    timestamp_str = utc_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return timestamp_str


def sort_by_timestamp(element):
    return element['timestamp']['us']


def trace_processing(traces):
    grouped_trace = {}
    # 以trace id为key，创建字典，存储data['_source']的内容
    for trace in traces:
        trace_id = trace['_source']['trace']['id']
        if trace_id in grouped_trace:
            grouped_trace[trace_id].append(trace['_source'])
        else:
            grouped_trace[trace_id] = [trace['_source']]

    timestamp_list = []
    cmdb_id_list = []
    span_id_list = []
    trace_id_list = []
    duration_list = []
    type_list = []
    status_code_list = []
    operation_name_list = []
    parent_span_id = []

    # 将grouped_trace中每个trace id下的list按照时间戳从小到大排序
    for trace_id, trace_list in grouped_trace.items():
        trace_list = sorted(trace_list, key=sort_by_timestamp)
        # 从每条trace中提取出需要的数据
        for trace in trace_list:
            try:
                # 判断processor下的name是span还是transaction
                processor_name = trace['processor']['event']
                if 'health' in trace[processor_name]['name'] or 'POST unknown route' in trace[processor_name]['name']:
                    continue
                span_id_list.append(trace[processor_name]['id'])
                duration_list.append(trace[processor_name]['duration']['us'])
                type_list.append(trace[processor_name]['type'])
                operation_name_list.append(trace[processor_name]['name'])
                timestamp_list.append(trace['timestamp']['us'])
                cmdb_id_list.append(trace['service']['name'])
                trace_id_list.append(trace_id)
                # 判断status_code是否存在
                if 'http' in trace:
                    if 'response' in trace['http']:
                        if 'status_code' in trace['http']['response']:
                            status_code_list.append(trace['http']['response']['status_code'])
                        else:
                            status_code_list.append(0)
                    else:
                        status_code_list.append(0)
                else:
                    status_code_list.append(0)
                # 判断parent_id是否存在
                if 'parent' in trace:
                    parent_span_id.append(trace['parent']['id'])
                else:
                    parent_span_id.append('')
            except Exception as e:
                print(trace)

    # 创建dataframe
    df = pd.DataFrame({
        'timestamp': timestamp_list,
        'cmdb_id': cmdb_id_list,
        'span_id': span_id_list,
        'trace_id': trace_id_list,
        'duration': duration_list,
        'type': type_list,
        'status_code': status_code_list,
        'operation_name': operation_name_list,
        'parent_span': parent_span_id
    })

    return df


def calculate_duration(trace):
    endTime = 0
    startTime = trace[0]['timestamp']['us']

    for item in trace:
        try:
            processor_name = item['processor']['event']
            if item['timestamp']['us'] < startTime:
                startTime = item['timestamp']['us']

            if item[processor_name]['duration']['us'] + item['timestamp']['us'] > endTime:
                endTime = item[processor_name]['duration']['us'] + item['timestamp']['us']
        except:
            print(item)

    totalDuration = endTime - startTime
    return totalDuration


# trace列表数据
def trace_data(traces):
    grouped_trace = {}
    # 以trace id为key，创建字典，存储data['_source']的内容
    for trace in traces:
        trace_id = trace['_source']['trace']['id']
        if trace_id in grouped_trace:
            grouped_trace[trace_id].append(trace['_source'])
        else:
            grouped_trace[trace_id] = [trace['_source']]

    result = []
    # 将grouped_trace中每个trace id下的list按照时间戳从小到大排序，并构建字典
    for trace_id, trace_list in grouped_trace.items():
        trace_list = sorted(trace_list, key=sort_by_timestamp)
        status_code_list = []
        # 从每条span中提取出status_code
        is_health = False
        for span in trace_list:
            try:
                # 判断processor下的name是span还是transaction
                processor_name = span['processor']['event']
                if 'health' in span[processor_name]['name'] or 'POST unknown route' == span[processor_name]['name']:
                    is_health = True
                    break
                # 判断status_code是否存在
                if 'http' in span:
                    if 'response' in span['http']:
                        if 'status_code' in span['http']['response']:
                            status_code_list.append(span['http']['response']['status_code'])
                        else:
                            status_code_list.append(0)
                    else:
                        status_code_list.append(0)
                else:
                    status_code_list.append(0)
            except Exception as e:
                print('error')
        if is_health:
            continue
        flag = 1
        for status_code in status_code_list:
            if status_code != 200 and status_code != 0:
                flag = 0
                break
        if flag == 1:
            status = 'Success'
        else:
            status = 'Error'

        try:
            # 获取第一个span的operation_name和timestamp
            first_span = trace_list[0]
            duration = calculate_duration(trace_list)
            processor_name = first_span['processor']['event']
            operation_name = first_span[processor_name]['name']
            timestamp = first_span['timestamp']['us']
        except Exception as e:
            print(e, trace_list)
        if (operation_name != 'POST unknown route'):
            result.append({
                'trace_id': trace_id,
                'duration': duration,
                'operation_name': operation_name,
                'timestamp': timestamp,
                'status': status,
            })
    return result


def traceId_data(traces):
    traces = [item['_source'] for item in traces]
    span_list = []
    span_list = [span_list.extend(item) for item in traces]
    print('traces', span_list)

    result = []
    # 将traces中每个span按照时间戳从小到大排序
    traces = sorted(traces, key=sort_by_timestamp)

    for span in traces:
        # 从每条trace中提取出需要的数据
        try:
            # 判断processor下的name是span还是transaction
            processor_name = span['processor']['event']
            if 'health' in span[processor_name]['name'] or 'POST unknown route' == span[processor_name]['name']:
                continue
            span_id = span[processor_name]['id']
            duration = span[processor_name]['duration']['us']
            type = span[processor_name]['type']
            operation_name = span[processor_name]['name']
            timestamp = span['timestamp']['us']
            cmdb_id = span['service']['name']
            # 判断status_code是否存在
            if 'http' in span:
                if 'response' in span['http']:
                    if 'status_code' in span['http']['response']:
                        status_code = span['http']['response']['status_code']
                    else:
                        status_code = 0
                else:
                    status_code = 0
            else:
                status_code = 0
            # 判断parent_id是否存在
            if 'parent' in span:
                parent_span_id = span['parent']['id']
            else:
                parent_span_id = ''
        except Exception as e:
            print(span)

        result.append({
            'timestamp': timestamp,
            'cmdb_id': cmdb_id,
            'span_id': span_id,
            'duration': duration,
            'type': type,
            'status_code': status_code,
            'operation_name': operation_name,
            'parent_span': parent_span_id
        })

    return result

class TraceAPI:
    def __init__(self, url: str, username: str, password: str):
        self.indices_template = monitor_config['trace_index']
        if root_config['es_use_cert'] == 'True':
            context = create_default_context(cafile=root_config['es_cert_path'])
            self.elastic = Elasticsearch(
                [url],
                http_auth=(username, password),
                timeout=60,
                max_retries=5,
                retry_on_timeout=True,
                ssl_context=context
            )
        else:
            self.elastic = Elasticsearch(
                [url],
                basic_auth=(username, password),
                verify_certs=False,
                timeout=60,
                max_retries=5,
                retry_on_timeout=True
            )

    # trace查找功能
    def query(self, start_time: Union[int, datetime, str, None], end_time: Union[int, datetime, str, None]):
        # 处理 start_time
        if isinstance(start_time, str):
            start_time = int(start_time)
        # 处理 end_time
        if isinstance(end_time, str):
            end_time = int(end_time)

        start_time = datetime.fromtimestamp(start_time)
        end_time = datetime.fromtimestamp(end_time)

        start_time = timezone_adjust(start_time)
        end_time = timezone_adjust(end_time)

        query_size = 5000
        # 定义Elasticsearch查询
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start_time,
                                    "lte": end_time
                                }
                            }
                        }
                    ]
                }
            },
            "sort": {
                "@timestamp": {
                    "order": "asc"
                }
            },
            "size": query_size
        }

        # 使用Elasticsearch搜索查询并返回结果
        data = []

        try:
            page = self.elastic.search(index=self.indices_template, body=query, scroll='15s')

            data.extend(page["hits"]["hits"])
            scroll_id = page['_scroll_id']

            while True:
                page = self.elastic.scroll(scroll_id=scroll_id, scroll='15s')
                hits_len = len(page["hits"]["hits"])
                data.extend(page["hits"]["hits"])
                if hits_len < query_size:
                    break
                scroll_id = page["_scroll_id"]
        except ConnectionTimeout as e:
            print('Connection Timeout:', e)
        df = trace_data(data)
        return df

    # 根据trace_id进行搜索
    def trace_byId(self, trace_id: str):
        query_size = 5000
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "trace.id": trace_id
                            }
                        }
                    ]
                }
            },
            "size": query_size
        }
        # 使用Elasticsearch搜索查询并返回结果
        data = []
        try:
            page = self.elastic.search(index=self.indices_template, body=query, scroll='15s')

            data.extend(page["hits"]["hits"])
            scroll_id = page['_scroll_id']

            while True:
                page = self.elastic.scroll(scroll_id=scroll_id, scroll='15s')
                hits_len = len(page["hits"]["hits"])
                data.extend(page["hits"]["hits"])
                if hits_len < query_size:
                    break
                scroll_id = page["_scroll_id"]
        except ConnectionTimeout as e:
            print('Connection Timeout:', e)
        df = traceId_data(data)
        return df

    def trace_extract(self, start_time=None, end_time=None, path=None):
        time_interval = 5 * 60
        csv_list = []
        os.makedirs(path, exist_ok=True)
        while start_time < end_time:
            current_end_time = start_time + time_interval
            if current_end_time > end_time:
                current_end_time = end_time
            data = self.trace_extract_(start_time=start_time, end_time=current_end_time)
            if len(data) != 0:
                data.to_csv(f'{path}/trace-{start_time}_{current_end_time}.csv', index=False)
                csv_list.append(f'{path}/trace-{start_time}_{current_end_time}.csv')
            start_time = current_end_time
            time.sleep(1)
        merge_csv(path, csv_list, 'trace')

    # trace数据导出
    def trace_extract_(self, start_time=None, end_time=None):
        trace_query_size = 5000

        if isinstance(start_time, int):
            start_time = datetime.fromtimestamp(start_time)
        if isinstance(end_time, int):
            end_time = datetime.fromtimestamp(end_time)

        start_time = timezone_adjust(start_time)
        end_time = timezone_adjust(end_time)

        query = {
            "size": trace_query_size,
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start_time,
                                    "lte": end_time
                                }
                            }
                        }
                    ]
                }
            },
            "sort": ["_doc"]
        }
        data = []

        st_time = time.time()
        try:
            page = self.elastic.search(index=self.indices_template, body=query, scroll='15s')

            data.extend(page["hits"]["hits"])
            scroll_id = page['_scroll_id']

            while True:
                page = self.elastic.scroll(scroll_id=scroll_id, scroll='15s')
                hits_len = len(page["hits"]["hits"])
                data.extend(page["hits"]["hits"])
                if hits_len < trace_query_size:
                    break
                scroll_id = page["_scroll_id"]
                time.sleep(1)

        except ConnectionTimeout as e:
            print('Connection Timeout:', e)

        df = trace_processing(data)
        ed_time = time.time()
        print('run time: ', ed_time - st_time)
        return df
