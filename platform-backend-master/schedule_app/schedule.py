from datetime import *
import time
import pytz
from monitor_app.log_api import choose_index_template
import re
from monitor_app import log



def filter_indices_by_template(indices, index_template):
    pattern = re.compile(index_template.replace('*', '.*'))

    filtered_indices = [index for index in indices if pattern.match(index)]

    return filtered_indices

def choose_index_to_delete():
    # 获得当前时间戳和前十四天的时间戳
    all_indices = log.elastic.indices.get(index="logstash-*")

    all_indices_template = set()
    for index in all_indices:
        date_str = '.'.join(index.split('-')[1].split('.')[:-1])
        all_indices_template.add('logstash-' + date_str + '*')
    end_time = int(time.time())
    start_time = end_time - 14 * 24 * 60 * 60
    indices_template = choose_index_template(all_indices, start_time, end_time)
    delete_indices_template = all_indices_template - indices_template

    filtered_indices = []
    for index_template in delete_indices_template:
        filtered_indices.extend(filter_indices_by_template(all_indices, index_template))
    return filtered_indices

def delete_indices():
        print('begin delete index...')
        delete_indices = choose_index_to_delete()
        print('delete', delete_indices)
        for index in delete_indices:
            try:
                log.elastic.indices.delete(index=index)
            except ValueError:
                print('删除索引失败', ValueError)
