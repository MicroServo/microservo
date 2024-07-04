from yaml import full_load
import os
import pathlib
import sys
from monitor_app.metric_api import PrometheusAPI
from monitor_app.trace_api import TraceAPI
from monitor_app.log_api import logAPI
from chaosmesh_app.chaosmesh_api import ChaosMeshAPI
import shutil
from multiprocessing import Process
from .models import LeaderboardDataset
import mysql.connector
root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)
root_config = full_load(open(root_path / "config.yaml", "r"))
monitor_config = full_load(open(root_path / "monitor_config.yaml", "r"))

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

dataset_pool = create_pool('dataset')
record_pool = create_pool('record')

def collect_dataset(start_time, end_time, dataset_path):
    if isinstance(start_time, str):
        start_time = int(start_time)
    if isinstance(end_time, str):
        end_time = int(end_time)

    trace_path = os.path.join(dataset_path,'trace')
    log_path = os.path.join(dataset_path,'log')
    chaos_path = os.path.join(dataset_path,'groundtruth')

    try:
        # 实例化PrometheusAPI类对象并查询数据
        prom = PrometheusAPI(monitor_config["prometheusApi"])
        # 实例化traceAPI类对象并查询数据
        trace = TraceAPI(monitor_config['api'], monitor_config['username'], monitor_config['password'])
        # 实例化logAPI类对象并查询数据
        log = logAPI(monitor_config['api'], monitor_config['username'], monitor_config['password'])
        chaos_mesh = ChaosMeshAPI()

        trace.trace_extract(start_time, end_time, trace_path)
        log.log_extract(start_time, end_time, log_path)
        prom.export_all_metrics(start_time, end_time, dataset_path)
        chaos_mesh.ground_truth_extract(start_time, end_time, chaos_path)
    except Exception as e:
        print(e)
        shutil.rmtree(dataset_path)
        return

def get_connection(pool):
    return pool.get_connection()

def get_first_waiting_task(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM leaderboard_app_leaderboarddataset WHERE status = 'waiting' LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def update_task_status(task_id, status, pool, pid=None):
    connection = get_connection(pool)
    cursor = connection.cursor()
    cursor.execute("UPDATE leaderboard_app_leaderboarddataset SET status = %s, pid = %s WHERE id = %s", (status, pid, task_id))
    connection.commit()
    cursor.close()
    connection.close()

def execute(task):
    pool = create_pool(str(task['id']))
    connection = get_connection(pool)
    try:
        os.makedirs(task['dataset_path'])
        collect_dataset(task['start_time'], task['end_time'], task['dataset_path'])
    except Exception as e:
        print(e)
        update_task_status(task['id'], 'failed', pool)
        return

    update_task_status(task['id'], 'finished', pool)
    if connection.is_connected():
        connection.close()

def execute_dataset_collect_task():
    connection = get_connection(dataset_pool)
    task = get_first_waiting_task(connection)
    if task:
        p = Process(target=execute, args=(task,))
        p.start()
        update_task_status(task['id'], 'running', dataset_pool, p.pid)
        p.join()
