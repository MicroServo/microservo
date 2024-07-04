import sys
import pathlib
root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)
from mysql.connector import pooling
from yaml import full_load
from kubernetes import client, config
from datetime import *
import json
import pytz
import os
import random

root_config = full_load(open(root_path / "config.yaml", "r"))

def get_stressor_type(stressors):
    failure_type = list(stressors.keys())[0]
    return failure_type

def get_service_for_pod(cmdb_id_list):
    service_list = [cmdb_id.split('-')[0] for cmdb_id in cmdb_id_list]
    return service_list

def str2int_time(duration_str):
    units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

    if duration_str[-1] not in units:
        raise ValueError("Invalid time unit. Allowed units: 's', 'm', 'h', 'd'")
    
    try:
        seconds = int(duration_str[:-1]) * units[duration_str[-1]]
        return seconds
    except ValueError:
        raise ValueError("Invalid duration format. Expected format: '<number><unit>', e.g. '15m'")
    
class ChaosMeshAPI:
    def __init__(self):
        self.connection = None
        self.pool = self.create_pool()

        config.kube_config.load_kube_config(config_file=root_config['kubernetes_path'])
        self.v1 = client.CoreV1Api()

    def create_pool(self):
        # 创建连接池
        pool = pooling.MySQLConnectionPool(
            pool_name="chaosmesh",
            pool_size=32,  # 连接池允许的最大连接数
            host=root_config['host'],
            user=root_config['user'],
            password=root_config['password'],
            database=root_config['chaosmesh_database'],
            port=root_config['port']
        )
        return pool

    def connect_mysql(self):
        try:
            # 从连接池中获取连接
            connection = self.pool.get_connection()
            return connection
        except mysql.connector.Error as error:
            print("Error connecting to MySQL database:", error)
            return None
    
    def detection_mysql_connection(self):
        try:
            self.connection.ping(True, 10, 3)
            print('mysql connection is ok')
            return
        except Exception as e:
            print(f'mysql not connected :{e}')
        try:
            self.connect_mysql()
        except Exception as e:
            print(f'mysql connected failed :{e}')

    def get_pods_for_label(self, namespace, label):
        label_selector = f'app={label}'
        pods = self.v1.list_namespaced_pod(namespace, label_selector=label_selector)
        pods = pods.items
        pods = [pod.metadata.name for pod in pods]
        return pods

    def get_culprit_cmdb_id(self, cmdb_id_list, *selectors):
        culprit_cmdb_id_list = []
        for selector in selectors:
            if 'pods' in selector:
                pods = selector['pods'][selector['namespaces'][0]]
                culprit_cmdb_id_list.extend([pod for pod in pods if pod in cmdb_id_list])
            else:
                namespace = selector['namespaces'][0]
                label = selector['labelSelectors']['app']
                pods = self.get_pods_for_label(namespace=namespace, label=label)
                culprit_cmdb_id_list.extend(pods)
        return culprit_cmdb_id_list

    def find_duration_in_workflow(self, metadata):
        workflow = metadata['labels']['chaos-mesh.org/workflow']
        instance = '-'.join(metadata['labels']['chaos-mesh.org/controlled-by'].split('-')[:-1])
        # workflow
        query = "SELECT * FROM workflow_entities WHERE name = %s"
        # self.detection_mysql_connection()
        connection = self.connect_mysql()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (workflow,))
            workflow_result = cursor.fetchall()
            cursor.close()
            connection.close()

        workflow_result = workflow_result[0]['workflow']
        workflow_data = json.loads(workflow_result)
        templates = workflow_data['spec']['templates']
        case = [case for case in templates if case['name'] == instance]
        return case[0]['deadline']


    def feature_extract(self, experiment, cmdb_id_list, kind, metadata):
        service_list = []
        culprit_cmdb_id_list = []
        failure_type = ''
        duration = 0
        if 'duration' in experiment.keys():
            duration = str2int_time(experiment['duration'])
        else:
            duration = str2int_time(self.find_duration_in_workflow(metadata))
        
        if kind == 'NetworkChaos':
            failure_type = experiment['action']
            direction = experiment['direction']

            if direction == 'to':
                selector = experiment['selector']
                culprit_cmdb_id_list = self.get_culprit_cmdb_id(cmdb_id_list, selector)
            elif direction == 'from':
                target = experiment['target']['selector']
                culprit_cmdb_id_list = self.get_culprit_cmdb_id(cmdb_id_list, target)
            else:
                selector = experiment['selector']
                target = experiment['target']['selector']
                culprit_cmdb_id_list = self.get_culprit_cmdb_id(cmdb_id_list, selector, target)
        elif kind == 'PodChaos':
            failure_type = experiment['action']
            selector = experiment['selector']
            culprit_cmdb_id_list = self.get_culprit_cmdb_id(cmdb_id_list, selector)
        elif kind == 'StressChaos':
            failure_type = get_stressor_type(experiment['stressors'])
            selector = experiment['selector']
            culprit_cmdb_id_list = self.get_culprit_cmdb_id(cmdb_id_list, selector)

        service_list = get_service_for_pod(culprit_cmdb_id_list)
        return service_list, culprit_cmdb_id_list, failure_type, duration

    def group_by_object_id(self, start_date, end_date):
        query = f"SELECT * FROM events WHERE namespace = '{root_config['namespace']}' AND created_at >= '{start_date}' AND created_at < '{end_date}' AND reason='Applied'"
        # self.detection_mysql_connection()
        connection = self.connect_mysql()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()
            connection.close()
        # 创建一个空字典用于存储按object_id分组后的结果
        grouped_result = {}

        # 遍历result中的每行记录
        for row in result:
            object_id = row['object_id']

            temp = {}
            temp['object_id'] = object_id
            # 转换created_at为timestamp
            temp['created_at'] = int(datetime.timestamp(row['created_at']))
            temp['kind'] = row['kind']
            temp['cmdb_id'] = []
            
            # 如果object_id不存在于grouped_result中，则创建一个新的列表，并将当前记录添加到列表中
            if object_id not in grouped_result:
                grouped_result[object_id] = temp

            # 处理message字段
            message = row['message']
            message = message[len('Successfully apply chaos for '):]
            cmdb_id = message.split('/')[1].strip()
            
            grouped_result[object_id]['cmdb_id'].append(cmdb_id)
        return grouped_result

    def create_ground_truth(self, start_time, end_time):
        # self.detection_mysql_connection()
        start_date = datetime.fromtimestamp(start_time).replace(tzinfo=None)
        end_date = datetime.fromtimestamp(end_time).replace(tzinfo=None)
        grouped_result = self.group_by_object_id(start_date, end_date)
        
        ground_truth = []
        print(f'grouped_result length: {len(grouped_result)}')
        for object_id, row in grouped_result.items():
            ts = row['created_at']
            # experiments
            query = "SELECT * FROM experiments WHERE uid = %s"

            connection = self.connect_mysql()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (object_id,))
                experiments_result = cursor.fetchall()
                cursor.close()
                connection.close()

            if len(experiments_result) == 0:
                continue
            experiment_data = experiments_result[0]['experiment'] # 如果此处没有数据怎么办??
            experiment = json.loads(experiment_data)
            try:
                culprit_service_list, culprit_cmdb_id_list, failure_type, duration = self.feature_extract(experiment['spec'], row['cmdb_id'], row['kind'], experiment['metadata'])
            except Exception as e:
                print(e, experiment['metadata'], experiment['spec'], row['cmdb_id'], row['kind'])
                continue
            for service, cmdb_id in zip(culprit_service_list, culprit_cmdb_id_list):

                ground_truth.append({
                    'timestamp':ts,
                    'service':service,
                    'cmdb_id_list':cmdb_id,
                    'failure_type':failure_type,
                    'duration':duration
                })

        return ground_truth
    
    def ground_truth_extract(self, start_time, end_time, path):
        ground_truth = self.create_ground_truth(start_time, end_time)
        ground_truth = self.transform_groundtruth(ground_truth)
        json_ground_truth = json.dumps(ground_truth, ensure_ascii=False)
        groundtruth_path = f'{path}/groundtruth.json'
        # 检查路径是否存在，如果不存在则创建路径
        if not os.path.exists(os.path.dirname(groundtruth_path)):
            print("创建路径")
            os.makedirs(os.path.dirname(groundtruth_path))
        with open(groundtruth_path, 'w', encoding='utf-8') as json_file:
                json_file.write(json_ground_truth)

    def transform_groundtruth(self, ground_truth):
        # 初始化一个字典，其中的每个键对应一个空列表
        transformed_ground_truth = {
            'timestamp': [],
            'service': [],
            'cmdb_id': [],
            'failure_type': [],
            'duration': []
        }

        # 遍历原始列表，将每个条目的值追加到新字典的相应列表中
        for entry in ground_truth:
            transformed_ground_truth['timestamp'].append(entry['timestamp'])
            transformed_ground_truth['service'].append(entry['service'])
            transformed_ground_truth['cmdb_id'].append(entry['cmdb_id_list'])
            transformed_ground_truth['failure_type'].append(entry['failure_type'])
            transformed_ground_truth['duration'].append(entry['duration'])

        return transformed_ground_truth