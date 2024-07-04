from django.views import View
from django.http import StreamingHttpResponse
from django.http import FileResponse
from monitor_app.utils.extract import zip_dir
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from . import chaos_mesh
from platform_backend import ApiResponse
from chaosmesh_app.chaos import *
from .models import Fault
import os
import json
from datetime import *
from croniter import croniter
import re
import shutil
import random
# Create your views here.

def time_str_to_seconds(time_str):
    # 定义单位和对应的秒数
    units = {'ms': 0.001, 's': 1, 'm': 60, 'h': 3600}

    # 解析时间字符串
    matches = re.split(r'(\d+)', time_str)
    
    # 获取数字部分和单位部分
    value = matches[1]
    unit = matches[2]

    # 转换为秒
    seconds = int(value) * units[unit]

    return seconds

# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class ChaosMeshView(View):
    
    def create_ground_truth(request):
        if request.method == 'GET':
            try:
                start_time = int(request.GET.get('start_time'))
                end_time = int(request.GET.get('end_time'))
                ground_truth = chaos_mesh.create_ground_truth(start_time=start_time, end_time=end_time)
                return ApiResponse.success(data={'ground_truth': ground_truth})
            except Exception as e:
                return ApiResponse.error(message=f"Failed to retrieve historical faults:{e}")
        else:
            return ApiResponse.http_error()
    
        
    def inject_fault(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                print(data)
                message = fill_generate_yaml(data['data'])
                return ApiResponse.success(data={'message':message})
            except Exception as e:
                return ApiResponse.error(message=f"Inject fault failed:{e}")
        else:
            return ApiResponse.http_error()

    
    def delete_injection(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                name = data['name']
                message = delete_chaos(name)
                return ApiResponse.success(data={'message':message})
            except Exception as e:
                return ApiResponse.error(message=f"Delete fault failed:{e}")
        else:
            return ApiResponse.http_error()
        
    def fetch_injection(request):
        if request.method == 'GET':
            try:
                res = []
                faults = Fault.objects.all()
                for fault in faults:
                    create_time =  int(fault.create_time.timestamp())
                    res.append(
                        {
                            'name':fault.name,
                            'type':fault.fault_type,
                            'spec':json.loads(fault.spec),
                            'schedule':fault.schedule,
                            'create_time':create_time,
                        }
                    )
                return ApiResponse.success(data=res)
            except Exception as e:
                return ApiResponse.error(message=f"Fetch faults failed:{e}")
        else:
            return ApiResponse.http_error()

    def get_future_injection(request):
        if request.method == 'GET':
            try:
                start_time = int(request.GET.get('start_time'))
                end_time = int(request.GET.get('end_time'))
                start_time = datetime.fromtimestamp(start_time).replace(tzinfo=None)
                end_time = datetime.fromtimestamp(end_time).replace(tzinfo=None)
                ground_truth = []
                # 获取所有在时间范围内的故障对象
                faults = Fault.objects.all()
                for fault in faults:
                    if fault.inject_type == 'schedule':
                        # shedule代表是周期性的
                        # 解析 cron 表达式
                        iter = croniter(fault.schedule, start_time)

                        # 生成下一个执行时间，直到超出 end_time
                        while True:
                            next_time = iter.get_next(datetime)
                            if next_time > end_time:
                                break
                            
                            spec = json.loads(fault.spec)
                            ts = int(next_time.timestamp())
                            name = spec['name']
                            service = spec['app']
                            pods = spec['pods']
                            duration = spec['duration']
                            duration = time_str_to_seconds(duration)
                            for cmdb_id in pods:
                                ground_truth.append({
                                    'timestamp':ts,
                                    'name':name,
                                    'service':service,
                                    'cmdb_id_list':cmdb_id,
                                    'failure_type':fault.fault_type,
                                    'duration': duration
                                })
                    elif fault.inject_type == 'experiment':
                        # 不是的话，代表是一次性的
                        iter = croniter(fault.schedule, start_time)
                        next_time = iter.get_next(datetime)
                        if start_time <= next_time <= end_time:
                            spec = json.loads(fault.spec)

                            ts = int(next_time.timestamp())
                            name = spec['name']
                            service = spec['app']
                            pods = spec['pods']
                            duration = spec['duration']
                            duration = time_str_to_seconds(duration)
                            for cmdb_id in pods:
                                ground_truth.append({
                                    'timestamp':ts,
                                    'name':name,
                                    'service':service,
                                    'cmdb_id_list':cmdb_id,
                                    'failure_type':fault.fault_type,
                                    'duration':duration
                                })
                return ApiResponse.success(data={'ground_truth': ground_truth})
            except Exception as e:
                return ApiResponse.error(message=f"Fetch fault injection plan failed:{e}")
        else:
            return ApiResponse.http_error()
    
    def extract_ground_truth(request):
        if request.method == 'GET':
            start_time = int(request.GET.get('start_time'))
            end_time = int(request.GET.get('end_time'))
            random_number = random.randint(1, 100000000)

            path = f'./chaosmesh_app/temp/{random_number}'

            random_number = chaos_mesh.ground_truth_extract(start_time, end_time, path + '/groundtruth')

            zip_dir(path)

            shutil.rmtree(path)

            file_path = f'{path}.zip'
            file_name = os.path.basename(file_path)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
                response['Content-Type'] = 'application/zip'
            else:
                return ApiResponse.error(message="delete zip failed")
            os.remove(f'{path}.zip')
            return response
        else:
            return ApiResponse.http_error()


        