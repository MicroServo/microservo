import yaml
import os
import subprocess
from multiprocessing import Process
import pathlib
from .models import Fault
import json
from croniter import croniter
import time
from datetime import datetime
from yaml import full_load

root_path = pathlib.Path(__file__).parent.parent
chaosmesh_app_path = pathlib.Path(__file__).parent

root_config = full_load(open(root_path / "config.yaml", "r"))


def fill_generate_yaml(data):
    app_port_mapping = {
        'cartservice': 7070,
        'checkoutservice': 5050,
        'currencyservice': 7000,
        'emailservice': 5000,
        'frontend': 18080,
        'paymentservice': 50051,
        'productcatalogservice': 3550,
        'recommendationservice': 8080,
        'redis-cart': 6379,
        'shippingservice': 50051,
    }
    inject_type = data['inject_type'] #分为experiment和schedule两种
    template_folder = os.path.join(chaosmesh_app_path, 'experiment')
    filled_content = ""

    selected_template = data['selected_template']
    selected_template = selected_template + ".yaml"
    
    

    # 定义模板参数字典
    template_params = {
        'name': data.get('name', ''),
        'app': data.get('app', ''),
        'duration': data.get('duration', ''),
        'schedule': data.get('schedule', ''),
        'pods': data.get('pods', ''),
        'namespace': root_config['namespace'],
        #如果是network
        'latency': data.get('latency', ''),
        'correlation': int(data.get('correlation', 0)),  # 如果correlation键不存在，默认值为0
        'jitter': data.get('jitter', ''),
        'loss': int(data.get('loss', 0)),  # 注意loss和correlation都是由''包起来的！!
        'targetapp': data.get('targetapp', ''),
        'targetpods': data.get('targetpods', ''),

        # 如果是http delay
        'delay': data.get('delay', ''),

        #如果是http abort,需要加一个port
        'port': app_port_mapping.get(data['app'], 80),

        #如果是cpu或者memory
        'workers': int(data.get('workers',0)),
        'load': int(data.get('load',0)),
        'size': data.get('size',''),

    }

    # 这里是存入数据库
    schedule = data.get('schedule', '')
    fault = Fault.objects.filter(name=data.get('name'))
    if fault.exists():
        # 如果存在，则返回第一个匹配的fault对象
        fault = fault.first()
        raise Exception("已经存在该故障!")
    else:
        # 如果不存在，则创建一个新的fault对象
        fault = Fault.objects.create(
            name=data.get('name', ''),
            inject_type=inject_type,
            spec=json.dumps(template_params),
            schedule=schedule,
            fault_type=data.get('fault_type')
        )


    # 读取模板文件内容
    with open(os.path.join(template_folder, selected_template), 'r') as file:
        template_content = file.read()

    # 使用模板参数填充模板内容
    filled_content = template_content.format(**template_params)
    # 生成新的 YAML 文件
    output_filename = data['name'] + ".yaml"
    output_folder = os.path.join(chaosmesh_app_path, "injection")
    # 将字符串解析为 Python 对象
    python_object = yaml.safe_load(filled_content)
    output_file_path = os.path.join(output_folder, output_filename)
    with open(output_file_path, 'w') as output_file:
        yaml.dump(python_object, output_file)

    print(f"已生成文件: {output_filename}")

def delete_chaos(name):
    try:
        fault = Fault.objects.get(name=name)
    except Fault.DoesNotExist:
        return

    fault.delete()
    # 删除配置文件
    output_folder = os.path.join(chaosmesh_app_path, "injection")
    output_filename = name + ".yaml"
    output_file_path = os.path.join(output_folder, output_filename)
    os.remove(output_file_path)

def execute(name):
    output_folder = os.path.join(chaosmesh_app_path, "injection")
    output_filename = name + ".yaml"
    output_file_path = os.path.join(output_folder, output_filename)
    
    command = f"kubectl apply -f {output_file_path} -n {root_config['namespace']}"
    # 调用终端并输入命令
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    message = result.stdout
    if message == '':
        raise Exception(f"Chaos {name} execution fails.")
    print(message)

def execute_experiment_chaos():
    # 定时执行crontab到点的实验
    current_time = datetime.now()

    for fault in Fault.objects.all():
        if croniter.match(fault.schedule, current_time):
            process = Process(target=execute, args=(fault.name,))
            process.start()

def delete_experiment_chaos():
    current_time = datetime.now()

    for fault in Fault.objects.filter(inject_type='experiment'):
        if croniter(fault.schedule, current_time).get_prev(datetime):
            process = Process(target=delete_chaos, args=(fault.name,))
            process.start()