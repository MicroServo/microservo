from django.http import StreamingHttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from platform_backend import ApiResponse
from leaderboard_app.leaderboard_api import get_leaderboard_data, get_algorithms, get_all_records, \
create_record, add_new_algorithm, query_record_data, re_evaluation, create_dataset, query_dataset
# Create your views here.

# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class LeaderboardView:

    def get_all_medals(request):
        if request.method == 'GET':
            try:
                algorithm_type = request.GET.get("algorithm_type")
                results = get_leaderboard_data(algorithm_type)
                return ApiResponse.success(data=results)
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()

    def get_all_records(request):
        if request.method == 'GET':
            try:
                algorithm_type = request.GET.get("algorithm_type")
                records = get_all_records(algorithm_type)
                return ApiResponse.success(data=records)
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()

    def create_record(request):
        if request.method == 'GET':
            try:
                record_name = request.GET.get("record_name")
                algorithm_type = request.GET.get("algorithm_type")
                dataset = request.GET.get("dataset")
                algorithm_list = request.GET.get("algorithm_list")
                create_person = request.user.username

                create_record(record_name, algorithm_type, dataset, algorithm_list, create_person)
                return ApiResponse.success()
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()

    def add_new_algorithm(request):
        if request.method == 'GET':
            try:
                record_id = request.GET.get("record_id")
                algorithm_list = request.GET.get("algorithm_list")

                add_new_algorithm(record_id, algorithm_list)
                return ApiResponse.success()
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()

    def query_record_data(request):
        if request.method == 'GET':
            try:
                record_id = request.GET.get("record_id")
                results = query_record_data(record_id)
                print(results)
                return ApiResponse.success(data=results)
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()

    def re_evaluation(request):
        if request.method == 'GET':
            try:
                record_id = request.GET.get("record_id")
                algorithm_id = request.GET.get("algorithm")

                re_evaluation(record_id=record_id, algorithm_id=algorithm_id)
                return ApiResponse.success()
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()

    def get_algorithms(request):
        if request.method == 'GET':
            try:
                algorithm_type = int(request.GET.get("algorithm_type"))
                res = get_algorithms(algorithm_type)
                return ApiResponse.success(data=res)
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()
        
    def create_dataset(request):
        if request.method == 'GET':
            try:
                start_time = int(request.GET.get("start_time"))
                end_time = int(request.GET.get("end_time"))
                dataset_name = request.GET.get("dataset_name")

                create_dataset(start_time, end_time, dataset_name, request.user.username)
                return ApiResponse.success()
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()
        
    def query_dataset(request):
        if request.method == 'GET':
            try:
                res = query_dataset()
                return ApiResponse.success(data=res)
            except Exception as e:
                print(e)
                return ApiResponse.error(e)
        else:
            return ApiResponse.http_error()