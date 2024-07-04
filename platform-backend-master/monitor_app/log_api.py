import json
import os
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Union

import pandas as pd
import pytz
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout

from . import pod_list as log_pod_list
from .utils.extract import merge_csv
from . import root_config
from ssl import create_default_context


def message_extract(json_str):
    message = json_str
    try:
        if 'severity' in json_str:
            data = json.loads(json_str)
            message = ''.join(['severity:', data['severity'], ',', 'message:', data['message']])
        elif 'level' in json_str:
            data = json.loads(json_str)
            message = ''.join(['level:', data['level'], ',', 'message:', data['message']])
    except:
        pass
    return message


def log_processing(logs):
    log_id_list = []
    ts_list = []
    date_list = []
    pod_list = []
    ms_list = []
    for log in logs:
        try:
            cmdb_id = log['_source']['kubernetes']['pod']['name']
            if cmdb_id not in log_pod_list:
                continue
            timestamp = log['_source']['@timestamp']
            timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
            timestamp = timestamp.timestamp()
            format_ts = log['_source']['@timestamp']
            message = message_extract(log['_source']['message'])
        except Exception as e:
            continue
        log_id_list.append(log['_id'])
        pod_list.append(cmdb_id)
        date_list.append(format_ts)
        ts_list.append(timestamp)
        ms_list.append(message)
    dt = pd.DataFrame({
        'log_id': log_id_list,
        'timestamp': ts_list,
        'date': date_list,
        'cmdb_id': pod_list,
        'message': ms_list
    })
    return dt


def log_for_query_filter(logs):
    filtered_log = []
    for log in logs:
        try:
            cmdb_id = log['_source']['kubernetes']['pod']['name']
            if cmdb_id not in log_pod_list:
                continue
        except Exception as e:
            continue
        filtered_log.append(log)
    return filtered_log


def choose_index_template(indices, start_time, end_time):
    indices_template = set()
    for index in indices:
        date_str = '.'.join(index.split('-')[1].split('.')[:-1])
        indices_template.add('logstash-' + date_str + '*')

    start_datetime_utc = datetime.fromtimestamp(start_time)
    end_datetime_utc = datetime.fromtimestamp(end_time)

    dates_in_range = set()
    current_datetime = start_datetime_utc

    while current_datetime <= end_datetime_utc:
        dates_in_range.add('logstash-' + current_datetime.strftime("%Y.%m.%d") + '*')
        current_datetime += timedelta(days=1)

    dates_in_range.add('logstash-' + end_datetime_utc.strftime("%Y.%m.%d") + '*')

    selected_patterns = indices_template.intersection(dates_in_range)

    return selected_patterns


# :param node: 指定集群节点
# :param pod: 指定pod名称
# :param start_time: 开始时间
# :param end_time: 截止时间
# :return: 日志list

class logAPI:
    def __init__(self, url: str, username: str, password: str):
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

    def query(self, start_time: Union[int, datetime, str], end_time: Union[int, datetime, str]):
        # 处理 start_time
        if isinstance(start_time, str):
            start_time = int(start_time)
        # 处理 end_time
        if isinstance(end_time, str):
            end_time = int(end_time)

        # 获取时间段内需要使用的indices
        indices = self.elastic.indices.get(index="logstash-*")
        indices = choose_index_template(indices, start_time, end_time)

        start_time = datetime.fromtimestamp(start_time)
        end_time = datetime.fromtimestamp(end_time)

        query_size = 2500
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

        for index in indices:
            try:
                page = self.elastic.search(index=index, body=query, scroll='15s')
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
        data = log_for_query_filter(data)
        print('len data', len(data))
        return data

    def log_extract(self, start_time=None, end_time=None, path=None):
        time_interval = 5 * 60
        csv_list = []
        os.makedirs(path, exist_ok=True)
        while start_time < end_time:
            current_end_time = start_time + time_interval
            if current_end_time > end_time:
                current_end_time = end_time
            data = self.log_extract_(start_time=start_time, end_time=current_end_time)
            if len(data) != 0:
                # 临时导出
                data.to_csv(f'{path}/log-{start_time}_{current_end_time}.csv', index=False)
                csv_list.append(f'{path}/log-{start_time}_{current_end_time}.csv')
            start_time = current_end_time
            time.sleep(1)

        merge_csv(path, csv_list, 'log')

    # log数据导出功能
    def log_extract_(self, start_time=None, end_time=None):

        quert_size = 7500

        # 获取时间段内需要使用的indices
        indices = self.elastic.indices.get(index="logstash-*")
        indices = choose_index_template(indices, start_time, end_time)
        print('indices', indices)

        if isinstance(start_time, int):
            start_time = datetime.fromtimestamp(start_time)
        if isinstance(end_time, int):
            end_time = datetime.fromtimestamp(end_time)
        query = {
            "size": quert_size,
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
        for index in indices:
            try:
                page = self.elastic.search(index=index, body=query, scroll='15s')

                data.extend(page["hits"]["hits"])
                scroll_id = page['_scroll_id']

                while True:
                    page = self.elastic.scroll(scroll_id=scroll_id, scroll='15s')
                    hits_len = len(page["hits"]["hits"])
                    data.extend(page["hits"]["hits"])
                    if hits_len < quert_size:
                        break
                    scroll_id = page["_scroll_id"]

            except ConnectionTimeout as e:
                print('Connection Timeout:', e)

        print('search time: ', time.time() - st_time)
        st_time = time.time()
        data = log_processing(data)
        print('process time:', time.time() - st_time)
        return data

    def get_log_number_by_day(self, time_select):
        data = []
        try:
            indices = self.elastic.indices.get(index="logstash-*")

            logs_per_day = {}  # 用于存储每天的日志数量

            # ONE_DAY 近一天按小时聚集
            if time_select == TimeSelect.ONE_DAY:
                for index in indices:
                    response = self.elastic.count(index=index)
                    index_date_str = index.split('-')[-1]  # 获取日期部分
                    index_date = datetime.strptime(index_date_str, "%Y.%m.%d.%H")  # 将索引日期部分转换为日期对象
                    # 如果在过去1天内
                    if index_date >= datetime.now() - timedelta(days=1):
                        # day_key = index_date.strftime("%Y-%m-%d")  # 将日期对象转换为 %Y-%m-%d 格式的字符串作为键

                        if index_date not in logs_per_day:
                            logs_per_day[index_date] = 0
                        logs_per_day[index_date] += response['count']
            elif time_select == TimeSelect.ONE_WEEK:
                for index in indices:
                    response = self.elastic.count(index=index)
                    index_date_str = index.split('-')[-1]  # 获取日期部分
                    index_date = datetime.strptime(index_date_str, "%Y.%m.%d.%H")  # 将索引日期部分转换为日期对象

                    # 如果在过去7天内
                    if index_date >= datetime.now() - timedelta(days=7):
                        day_key = index_date.strftime("%Y-%m-%d")  # 将日期对象转换为 %Y-%m-%d 格式的字符串作为键

                        if index_date not in logs_per_day:
                            logs_per_day[day_key] = 0
                        logs_per_day[day_key] += response['count']
            elif time_select == TimeSelect.TWO_WEEK:
                for index in indices:
                    response = self.elastic.count(index=index)
                    index_date_str = index.split('-')[-1]  # 获取日期部分
                    index_date = datetime.strptime(index_date_str, "%Y.%m.%d.%H")  # 将索引日期部分转换为日期对象

                    # 如果在过去14天内
                    if index_date >= datetime.now() - timedelta(days=14):
                        day_key = index_date.strftime("%Y-%m-%d")  # 将日期对象转换为 %Y-%m-%d 格式的字符串作为键

                        if index_date not in logs_per_day:
                            logs_per_day[day_key] = 0
                        logs_per_day[day_key] += response['count']
            else:
                print(f"Wrong input params: {time_select}")
                return data
            # 整理数据
            for date_str, log_count in logs_per_day.items():
                data.append({
                    "date": date_str,
                    "log_count": log_count
                })
        except ConnectionTimeout as e:
            print('Connection Timeout:', e)
        return data


class TimeSelect(Enum):
    ONE_DAY = 1
    ONE_WEEK = 2
    TWO_WEEK = 3

    @classmethod
    def get_item_by_value(cls, enum_type, value):
        for member in enum_type.__members__.values():
            if member.value == int(value):
                return member
        return ValueError(f"no member found with value : {value}")

