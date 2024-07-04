from .models import LeaderboardOverall, LeaderboardRecord, LeaderboardDataset
from algorithm_app.models import Algorithm, EvaluationIndicator, TaskTemplate, TaskExecute
import docker
import docker.errors
import json
from yaml import full_load
import os
import pathlib
import sys
from django.utils import timezone
from algorithm_app.task import calculate_evaluation_metrics
from platform_backend import ApiResponse
root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)
root_config = full_load(open(root_path / "config.yaml", "r"))


def get_leaderboard_data(algorithm_type):
    # 获取指定 algorithm_type 的所有算法和评价指标
    algorithms = Algorithm.objects.filter(algorithm_type_id=algorithm_type)
    evaluation_indicators = EvaluationIndicator.objects.filter(algorithm_type_id=algorithm_type)

    # 初始化结果字典
    results = {}
    for algorithm in algorithms:
        if algorithm.algorithm_name not in results:
            results[algorithm.algorithm_name] = {}

        for indicator in evaluation_indicators:
            results[algorithm.algorithm_name][indicator.indicator_name] = {
                "gold": 0,
                "silver": 0,
                "copper": 0,
                "strawberry": 0,
                "total": 0
            }

    # 获取指定 failure_type 的所有记录
    data = LeaderboardOverall.objects.filter(algorithm_type_id=algorithm_type)
    
    # 更新字典数据
    for item in data:
        algorithm_name = item.algorithm.algorithm_name  # 确保使用正确的属性来获取名称
        indicator_name = item.evaluation_metric.indicator_name
        
        results[algorithm_name][indicator_name]["gold"] += item.gold or 0
        results[algorithm_name][indicator_name]["silver"] += item.silver or 0
        results[algorithm_name][indicator_name]["copper"] += item.copper or 0
        results[algorithm_name][indicator_name]["strawberry"] += item.strawberry or 0
        results[algorithm_name][indicator_name]["total"] += item.total or 0

    # 将结果添加到列表中
    list_results = []
    for algorithm_name, indicators in results.items():
        algorithm_result = {"algorithm": algorithm_name}
        for indicator_name, values in indicators.items():
            algorithm_result[indicator_name] = values
        list_results.append(algorithm_result)

    return list_results

def get_all_records(algorithm_type):
    records = LeaderboardRecord.objects.filter(algorithm_type_id=algorithm_type)

    res = []
    for record in records:
        res.append(
            {
                'record_name': record.record_name,
                'record_id': record.id,
                'dataset': record.dataset.dataset_name,
                'algorithm_list': record.algorithms
            }
        )
    return res

def get_algorithms(algorithm_type):
    algorithms = Algorithm.objects.filter(algorithm_type_id=algorithm_type, container_status=True)

    res = []
    for algorithm in algorithms:
        res.append(
            {
                "id": algorithm.id,
                "algorithm_name": algorithm.algorithm_name
            }
        )
    return res

def create_record(record_name, algorithm_type, dataset, algorithm_list, create_person):
    record = LeaderboardRecord.objects.create(
        record_name=record_name,
        algorithm_type_id=algorithm_type,
        dataset_id=dataset,
        algorithms=algorithm_list,
        create_person=create_person
    )

    # 将任务提交
    submit_record_task(record.id)

def submit_record_task(record_id):
    record = LeaderboardRecord.objects.get(id=record_id)
    algorithm_list = record.algorithms.split(',')

    for algorithm_id in algorithm_list:
        task_template = TaskTemplate.objects.create(
            algorithm_id=algorithm_id,
            is_evaluate='True',
            record_id=record_id,
            create_person=record.create_person
        )
        execute_evaluate_template(task_template.id)

def execute_evaluate_template(template_id):
    task_template = TaskTemplate.objects.get(id=template_id)
    record = LeaderboardRecord.objects.get(id=task_template.record_id)
    task_name = 'record_' + str(record.id) + '_' + task_template.algorithm.algorithm_name
    dataset_range = record.dataset.id
    execute_type = '0' # 立即or定时 0 or 1
    execute_status = 'waiting'
    execute_person = record.create_person
    start_time = timezone.now()

    if not task_template.algorithm.container_created:
        return ApiResponse.error(message="该模版使用算法容器已删除，无法执行")
    # 判断算法是否是拆分的
    train_or_test = None
    if task_template.algorithm.is_split:
        train_or_test = "test"
    TaskExecute.objects.create(
        template_id=template_id,
        task_name=task_name,
        dataset_range=dataset_range,
        execute_type=execute_type,
        execute_status=execute_status,
        execute_person=execute_person,
        start_time=start_time,
        train_or_test=train_or_test
    )

def add_new_algorithm(record_id, algorithm_list):
    record = LeaderboardRecord.objects.get(id=record_id)
    record.algorithms += "," + algorithm_list
    record.save()

    algorithm_list = algorithm_list.split(',')

    for algorithm_id in algorithm_list:
        task_template = TaskTemplate.objects.create(
            algorithm_id=algorithm_id,
            is_evaluate='True',
            record_id=record_id,
            create_person=record.create_person
        )
        execute_evaluate_template(task_template.id)

def query_record_data(record_id):
    record = LeaderboardRecord.objects.get(id=record_id)
    json_data = record.result
    results = json.loads(json_data) if json_data else {}
    algorithm_type_id = record.algorithm_type.id
    algorithm_type = record.algorithm_type.name
    evaluation_metrics = []
    indicators = EvaluationIndicator.objects.filter(algorithm_type_id=algorithm_type_id)
    for indicator in indicators:
        evaluation_metrics.append({
            "indicator_name": indicator.indicator_name,
            "indicator_format": indicator.format_json
        })
    # 将结果添加到列表中
    list_results = []
    for algorithm_id, result in results.items():
        algorithm_result = {"algorithm": algorithm_id}
        if result is not None and len(result) != 0:
            for evaluate_metric in evaluation_metrics:
                new_result = calculate_evaluation_metrics(result, algorithm_type, evaluate_metric)
                algorithm_result[evaluate_metric['indicator_name']] = new_result
        list_results.append(algorithm_result)

    return list_results

def re_evaluation(record_id, algorithm_id):
    print(record_id, algorithm_id)
    record = LeaderboardRecord.objects.get(id=record_id)
    # 复用任务提交的接口
    task_template = TaskTemplate.objects.create(
        algorithm_id=algorithm_id,
        is_evaluate='True',
        record_id=record_id,
        create_person=record.create_person
    )
    execute_evaluate_template(task_template.id)
    
def create_dataset(start_time, end_time, dataset_name, user):
    dataset_path = os.path.join(root_config['dataset_dir'], dataset_name)
    
    LeaderboardDataset.objects.create(
        dataset_name=dataset_name,
        dataset_path=dataset_path,
        status='waiting',
        start_time=start_time,
        end_time=end_time,
        create_person=user
    )

def query_dataset():
    datasets = LeaderboardDataset.objects.all()

    res = []

    for dataset in datasets:
        res.append({
            'id': dataset.id,
            'dataset_name': dataset.dataset_name,
            'status': dataset.status,
            'create_person': dataset.create_person,
            'create_time': dataset.create_time
        })
    
    return res