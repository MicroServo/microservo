import os
import shutil
import random

from django.http import StreamingHttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from platform_backend import ApiResponse
from . import log, trace, prom, pod_list
from .log_api import TimeSelect
from .utils.extract import zip_dir
from . import root_config


# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class MonitorView(View):

    def query_log_data(request):
        if request.method == 'GET':
            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')
            data = log.query(start_time=start_time, end_time=end_time)
            if not data:
                return ApiResponse.error(message='No data found.')
            # 根据需要格式化或转换data值
            return ApiResponse.success(data=data)
        else:
            return ApiResponse.http_error()

    def extract_log(request):
        if request.method == 'GET':
            start_time = int(request.GET.get('start_time'))
            end_time = int(request.GET.get('end_time'))
            random_number = random.randint(1, 100000000)
            
            path = f'./monitor_app/temp/{random_number}'
            log.log_extract(start_time, end_time, path + '/log')
            zip_dir(path)
            shutil.rmtree(path)
            file_path = f'{path}.zip'
            file_name = os.path.basename(file_path)

            def file_iterator(file_path, chunk_size=512):
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data

            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)
            response['Content-Type'] = 'application/zip'
            return response
        else:
            return ApiResponse.http_error()

    def query_log_num(request):
        if request.method == 'GET':
            value = request.GET.get("time_select")
            time_select = TimeSelect.get_item_by_value(TimeSelect, value)
            data = log.get_log_number_by_day(time_select)
            if not data:
                return ApiResponse.error('No data found.')
            else:
                # 根据需要格式化或转换data值
                return ApiResponse.success(data=data)
        else:
            return ApiResponse.http_error()

    def query_trace_data(request):
        if request.method == 'GET':
            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')
            data = trace.query(start_time=start_time, end_time=end_time)
            if len(data) == 0:
                return ApiResponse.error(message='No data found.')
            else:
                # 根据需要格式化或转换data值
                return ApiResponse.success(data=data)
        else:
            return ApiResponse.http_error()

    def query_trace_byId(request):
        if request.method == 'GET':
            trace_id = request.GET.get('trace_id')
            data = trace.trace_byId(trace_id=trace_id)
            if len(data) == 0:
                return ApiResponse.error(message='No data found.')
            else:
                # 根据需要格式化或转换data值
                return ApiResponse.success(data=data)
        else:
            return ApiResponse.http_error()

    def extract_trace(request):
        if request.method == 'GET':
            start_time = int(request.GET.get('start_time'))
            end_time = int(request.GET.get('end_time'))
            random_number = random.randint(1, 100000000)

            path = f'./monitor_app/temp/{random_number}'
            trace.trace_extract(start_time, end_time, path + '/trace')
            zip_dir(path)
            shutil.rmtree(path)
            file_path = f'{path}.zip'
            file_name = os.path.basename(file_path)

            def file_iterator(file_path, chunk_size=512):
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data

            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)
            response['Content-Type'] = 'application/zip'
            return response

        else:
            return ApiResponse.http_error()

    def query_prometheus_data(request):
        if request.method == 'GET':

            pod = request.GET.get('pod')
            metric_name = request.GET.get('metric_name')
            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')
            data = prom.query_range(metric_name, pod, start_time=start_time, end_time=end_time, namespace=root_config['namespace'])

            if 'error' in data:
                return ApiResponse.error(message='Error in data.', data=data)
            else:
                # 根据需要格式化或转换data值
                return ApiResponse.success(data=data)
        else:
            return ApiResponse.http_error()

    def export_metric_data(request):
        if request.method == 'GET':
            start_time = int(request.GET.get('start_time'))
            end_time = int(request.GET.get('end_time'))
            step = int(request.GET.get('step'))
            random_number = random.randint(1, 100000000)

            path = f'./monitor_app/temp/{random_number}'
            random_number = prom.export_all_metrics(start_time, end_time, path + '/metric', step=step)
            zip_dir(path)

            shutil.rmtree(path)

            file_path = f'{path}.zip'
            file_name = os.path.basename(file_path)

            def file_iterator(file_path, chunk_size=512):
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data

            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)
            response['Content-Type'] = 'application/zip'
            return response
        else:
            return ApiResponse.http_error()

    def query_metric_name(request):
        if request.method == 'GET':
            metric_names = prom.get_all_metrics()
            return ApiResponse.success(data=metric_names)
        else:
            return ApiResponse.http_error()

    def get_pod_list(request):
        if request.method == 'GET':
            return ApiResponse.success(data=pod_list)
        else:
            return ApiResponse.http_error()




