from algorithm_app.models import TaskExecute,TaskTemplate,Algorithm
import subprocess
from django.utils import timezone
from multiprocessing import Process
import os
from monitor_app.metric_api import PrometheusAPI
from monitor_app.trace_api import TraceAPI
from monitor_app.log_api import logAPI
from chaosmesh_app.chaosmesh_api import ChaosMeshAPI
import pathlib
from yaml import full_load
import sys
import docker
import shutil
from leaderboard_app.models import LeaderboardRecord
import datetime
import mysql.connector
from evaluation.evaluation_metric import AnomalyDetection, RootCauseLocalization, FailureClassification
root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)
# 读取配置文件
monitor_config = full_load(open(root_path / "monitor_config.yaml", "r"))
root_config = full_load(open(root_path / "config.yaml", "r"))

def create_pool(pool_name):
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name=pool_name,
        pool_size=10,  # 池中保持的连接数
        pool_reset_session=True,
        host=root_config['host'],
        database=root_config['database'],
        user=root_config['user'],
        password=root_config['password'],
        port=root_config['port']
    )
    return pool

algorithm_pool = create_pool('algorithm')

def collect_data(dataset_path, dataset_type_array, start_time, end_time):
    trace_path = os.path.join(dataset_path,'trace')
    log_path = os.path.join(dataset_path,'log')
    chaos_path = os.path.join(dataset_path,'groundtruth')

    # 实例化PrometheusAPI类对象并查询数据
    prom = PrometheusAPI(monitor_config["prometheusApi"])
    # 实例化traceAPI类对象并查询数据
    trace = TraceAPI(monitor_config['api'], monitor_config['username'], monitor_config['password'])
    # 实例化logAPI类对象并查询数据
    log = logAPI(monitor_config['api'], monitor_config['username'], monitor_config['password'])
    chaos_mesh = ChaosMeshAPI()

    if 'trace' in dataset_type_array:
        trace.trace_extract(start_time, end_time, trace_path)
    if 'log' in dataset_type_array:
        log.log_extract(start_time, end_time, log_path)
    if 'metric' in dataset_type_array:
        prom.export_all_metrics(start_time, end_time, dataset_path)
    # 不管怎么样都要执行groundtruth
    chaos_mesh.ground_truth_extract(start_time, end_time, chaos_path)
    print("数据准备完毕!")

def get_connection(pool):
    return pool.get_connection()

def get_first_waiting_task(connection):
    # 获取当前时间，格式化为适合 SQL 查询的形式
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 创建查询，包括对 start_time 和 execute_status 的筛选
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM algorithm_app_taskexecute
    WHERE start_time <= %s AND execute_status = 'waiting'
    ORDER BY start_time ASC  # 可以根据需要对结果进行排序
    LIMIT 1
    """
    cursor.execute(query, (now,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def update_task_status(task_id, status, pool, pid=None, container_pid=None):
    connection = get_connection(pool)
    cursor = connection.cursor()
    cursor.execute("UPDATE algorithm_app_taskexecute SET execute_status = %s, pid = %s, container_pid = %s WHERE id = %s", (status, pid, container_pid, task_id))
    connection.commit()
    cursor.close()
    connection.close()

def execute(task, algorithm):
    pool = create_pool(str(task['id']))
    connection = get_connection(pool)
    try:
        user = task['execute_person']
        dataset_timestamp = str(int(task['create_time'].timestamp()))
        new_user = user + '_' + dataset_timestamp #这个是user+timestamp的新user
        dataset_path = algorithm['dataset_path'].replace("{user}", new_user)

        template_id = task['template_id']
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM algorithm_app_tasktemplate WHERE id = %s", (template_id,))
        template = cursor.fetchone()
        
        if template['is_evaluate'] == 'True':
            record_id = template['record_id']
            cursor.execute("SELECT * FROM leaderboard_app_leaderboardrecord WHERE id = %s", (record_id,))
            record = cursor.fetchone()
            dataset_id = record['dataset_id']
            cursor.execute("SELECT * FROM leaderboard_app_leaderboarddataset WHERE id = %s", (dataset_id,))
            dataset = cursor.fetchone()
            evalute_dataset_path = dataset['dataset_path']
            shutil.copytree(evalute_dataset_path, dataset_path)
        else:
            os.makedirs(dataset_path, exist_ok=True)
            start_time = int(task['dataset_range'].split(",")[0])
            end_time = int(task['dataset_range'].split(",")[1])
            if not start_time or not end_time:
                raise Exception("dataset_range有误")

            dataset_type = algorithm['dataset_type']
            dataset_type_array = dataset_type.split(",")
            collect_data(dataset_path, dataset_type_array, start_time, end_time)

        command = None
        if algorithm['is_split']:
            if task['train_or_test'] == "train":
                command = algorithm['train_command']
            elif task['train_or_test'] == "test":
                command = algorithm['test_command']
        else:
            command = algorithm['run_command']
        command = command.format(new_user,task['id'])
        print('command', command)
            # 然后用curl命令来执行任务 s
        res = subprocess.run(command, shell=True, capture_output=True, text=True)
    except Exception as e:
        update_task_status(task['id'], 'failed', pool)
        print(f"执行命令失败!{e}")
    cursor.close()
    connection.close()


def execute_timed_task():
    # try:
    connection = get_connection(algorithm_pool)
    # 获取第一个开始时间在当前时间之前且状态为未执行的任务
    task = get_first_waiting_task(connection)
    
    if task:
        # 先把该任务状态设为执行中
        connection = get_connection(algorithm_pool)
        # 获取 TaskTemplate
        template_id = task['template_id']
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM algorithm_app_tasktemplate WHERE id = %s", (template_id,))
        template = cursor.fetchone()

        algorithm_id = template['algorithm_id']

        # 获取 Algorithm
        cursor.execute("SELECT * FROM algorithm_app_algorithm WHERE id = %s", (algorithm_id,))
        algorithm = cursor.fetchone()

    
        cursor.close()
        connection.close()

        #先查询一下容器的状态
        # try:
        #     client = docker.from_env()
        #     container = client.containers.get(algorithm.algorithm_name)
        #     if container.status == "running":
        #         container_status = True
        #     else:
        #         container_status =False
        #     algorithm.container_status = container_status
        #     algorithm.save()
        # except docker.errors.APIError as e:
        #     pass
        if not algorithm['container_created'] or not algorithm['container_status']:
            update_task_status(task['id'], 'failed', algorithm_pool)
            raise Exception(f"执行任务失败!容器不在运行中或容器还未启动")
        
        process = Process(target=execute, args=(task, algorithm))
        process.start()
        update_task_status(task['id'], 'running', algorithm_pool, process.pid)

    # except Exception as e:
    #     print(f"定时执行任务失败!{e}")

def calculate_evaluation_metrics(result, algorithm_type, indicator, top_k=5):
    instance = globals()[algorithm_type](result)
    
    if algorithm_type == 'AnomalyDetection':
        result = instance.compute_metric_by_name(indicator['indicator_name'])
    elif algorithm_type == 'RootCauseLocalization':
        result = instance.compute_metric_by_name(indicator['indicator_name'], top_k)
    elif algorithm_type == 'FailureClassification':
        result = instance.compute_metric_by_name(indicator['indicator_name'])

    return result