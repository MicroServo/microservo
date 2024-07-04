import datetime
import io
import pathlib
import signal

import docker.errors
from django.core.paginator import Paginator

root_path = pathlib.Path(__file__).parent.parent
from .models import Algorithm, EvaluationIndicator, TaskTemplate, TaskExecute, AlgorithmType
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import FileResponse
from platform_backend import ApiResponse
import zipfile
import time
import json
import docker
import os
import multiprocessing
import subprocess
import shutil
import random
import string
from .task import calculate_evaluation_metrics


def seek_to_last_n_line(fi, n, buf_size=4096):

    now_line_cnt = 0
    output_start_pos = 0

    # 如果是空文件，那么直接返回即可
    read_pos = fi.seek(0, io.SEEK_END)
    if read_pos == 0:
        return

    # 检查最后一行是否以换行结尾。这里涉及到多一行还是少一行的边界情况处理
    fi.seek(read_pos-1)
    x = fi.read(1)
    if x == b"\n":
        now_line_cnt = -1

    # 算法主体部分，每次读取一个指定缓冲区大小的数据块，然后寻找换行符的个数
    run = True
    while run:
        read_pos = max(read_pos-buf_size, 0)
        fi.seek(read_pos)
        data = fi.read(buf_size)
        end_pos = len(data)

        # 在读取的缓冲区中从右向左查找换行符
        while 1:
            # rfind在底层是解释器用C语言实现的，效率非常高
            new_line_pos = data.rfind(b"\n", 0, end_pos)
            if new_line_pos == -1:
                if read_pos == 0:
                    run = False
                break

            end_pos = new_line_pos
            now_line_cnt += 1
            output_start_pos = read_pos + new_line_pos + 1
            if now_line_cnt == n:
                run = False
                break

    # 如果整个文件遍历到开头都没有满足行数要求，那就输出整个文件
    if now_line_cnt < n:
        output_start_pos = 0

    fi.seek(output_start_pos)
def stop_task(username,id):
    task_execute = TaskExecute.objects.get(id=id)

    if task_execute.execute_status == "waiting":
        raise Exception("Task has not been executed yet!")
    elif task_execute.execute_status == "finished":
        raise Exception("Task has been completed!")
    elif task_execute.execute_status == "interrupted":
        raise Exception("Task has been interrupted!")
    elif task_execute.execute_status == "failed":
        raise Exception("Task execution failed!")


    pid = None
    container_pid = None
    
    if task_execute.pid:
        pid = int(task_execute.pid)
    if task_execute.container_pid:
        container_pid = int(task_execute.container_pid)
    active_children = multiprocessing.active_children()
    p = None #获取后端的子进程
    
    for child in active_children:
        if child.pid == pid:
            p = child
    if p:
        p.terminate()
        print("Interrupt process successfully.")

    ip = task_execute.template.algorithm.container_ip
    port = task_execute.template.algorithm.container_port

    if container_pid:
        command = f'curl "http://{ip}:{port}/modelstop?user={username}&pid={container_pid}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        mes = result.stdout
        print(f"Interrupt process successfully.{mes}")

    #中断后更改数据库信息
    task_execute.execute_status = "interrupted"
    task_execute.pid = None
    task_execute.container_pid = None
    task_execute.save()

    message = "Interrupt successfully."

    return message

# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 POST
@require_http_methods(["POST", "GET"])
class TaskTemplateView(View):
    def get_algorithm_by_type(request):
        if request.method == 'GET':
            # 获取原始请求体数据
            algorithm_type = request.GET.get("type")
            if not algorithm_type:
                algorithm_list = Algorithm.objects.filter(container_created=True)
            else:
                algorithm_list = Algorithm.objects.filter(algorithm_type=algorithm_type, container_created=True)
            res = algorithm_list.values('id', 'algorithm_name')
            return ApiResponse.success(data=json.dumps(list(res)))
        else:
            return ApiResponse.http_error()

    def get_indicator_by_algorithm_type(request):
        if request.method == 'GET':
            try:
                algorithm_type_id = request.GET.get("id")
                indicators = EvaluationIndicator.objects.filter(algorithm_type_id=algorithm_type_id)
                res = []
                for indicator in indicators:
                    res.append({
                        'id': indicator.id,
                        'name': indicator.indicator_name
                    })
                return ApiResponse.success(data=res)
            except Exception as e:
                return ApiResponse.error(message=str(e))
        else:
            return ApiResponse.http_error()

    def task_template_create(request):
        if request.method == 'POST':
            raw_data = request.body
            # 解析Json数据
            data = json.loads(raw_data)
            template_name = data.get("template_name")
            algorithm_id = data.get("algorithm_id")
            indicator_id = data.get("indicator_id")
            create_person = request.user.username
            task_template = TaskTemplate.objects.create(template_name=template_name,
                                                        algorithm_id=algorithm_id,
                                                        indicator_id=indicator_id,
                                                        create_person=create_person,
                                                        is_evaluate='False')
            if not task_template:
                return ApiResponse.error(message="Create template failed.")
            return ApiResponse.success(message="Create template successfully.")
        else:
            return ApiResponse.http_error()

    def get_task_template_list(request):
        if request.method == 'GET':
            page = request.GET.get("page")
            page_size = request.GET.get("page_size")
            if not page or int(page) < 1:
                page = 1
            if not page_size:
                page_size = 20
            page = int(page)
            page_size = int(page_size)
            queryset = TaskTemplate.objects.filter(is_evaluate='False').order_by('create_time')
            paginator = Paginator(queryset, page_size)
            if page > paginator.num_pages:
                page = paginator.num_pages
            page_obj = paginator.page(page)
            info = []
            for obj in page_obj:
                try:
                    indicator = EvaluationIndicator.objects.get(id=obj.indicator_id)
                
                    info.append({"id": obj.id,
                        "template_name": obj.template_name,
                        "algorithm_type": obj.algorithm.algorithm_type_id,
                        "algorithm_name": obj.algorithm.algorithm_name,
                        "indicator": indicator.indicator_name,
                        "create_person": obj.create_person,
                        "create_time": obj.create_time
                        })
                except Exception as e:
                    info.append({"id": obj.id,
                        "template_name": obj.template_name,
                        "algorithm_type": obj.algorithm.algorithm_type_id,
                        "algorithm_name": obj.algorithm.algorithm_name,
                        "indicator": '',
                        "create_person": obj.create_person,
                        "create_time": obj.create_time
                        })

            res = {"total": paginator.count,
                   "num_pages": paginator.num_pages,
                   "current_page": page,
                   "page_size": page_size,
                   "info": info}
            return ApiResponse.success(data=res)
        else:
            return ApiResponse.http_error()

    def delete_task_template(request):
        if request.method == 'POST':
            try:
                raw_data = request.body
                # 解析Json数据
                data = json.loads(raw_data)
                ids = data.get("ids")
                id_list = ids.split(",")
                fail_task_template_list = []
                for id in id_list:
                    if TaskExecute.objects.filter(template_id=id, execute_status='running').count() > 0:
                        fail_task_template_list.append(TaskTemplate.objects.get(id=id).template_name)
                        continue
                    TaskExecute.objects.filter(template_id=id).delete()
                    TaskTemplate.objects.get(id=id).delete()
                if len(fail_task_template_list) == 0:
                    return ApiResponse.success(message="Delete template successfully")
                return ApiResponse.success(message=f"Template {fail_task_template_list} has a running task, can't delete.")
            except Exception as e:
                return ApiResponse.error(message=str(e))
        else:
            return ApiResponse.http_error()

    def delete_execute_task(request):
        if request.method == 'POST':
            try:
                raw_data = request.body
                # 解析Json数据
                data = json.loads(raw_data)
                ids = data.get("ids")
                id_list = ids.split(",")
                for id in id_list:
                    if TaskExecute.objects.get(id=id).execute_type == "running":
                        return ApiResponse.error(message="Running tasks cannot be deleted. Please stop the task before deleting it!")
                for id in id_list:
                    TaskExecute.objects.get(id=id).delete()
                return ApiResponse.success(message="Delete successfully.")
            except Exception as e:
                return ApiResponse.error(message=str(e))
        else:
            return ApiResponse.http_error()

    def get_task_execute_list(request):
        if request.method == 'GET':
            page = request.GET.get("page")
            page_size = request.GET.get("page_size")
            if not page or int(page) < 1:
                page = 1
            if not page_size:
                page_size = 20
            page = int(page)
            page_size = int(page_size)
            # 获取应该被排除的模板的ID
            excluded_template_ids = TaskTemplate.objects.filter(is_evaluate='True').values_list('id', flat=True)

            # 查询排除这些模板的所有执行
            queryset = TaskExecute.objects.exclude(template__id__in=excluded_template_ids).order_by('-create_time')
            paginator = Paginator(queryset, page_size)
            if page > paginator.num_pages:
                page = paginator.num_pages
            page_obj = paginator.page(page)
            info = [{'id': obj.id, 'name': obj.task_name, 'execute_status': obj.execute_status,
                     'create_person': obj.create_person,
                     'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S')} for obj in page_obj]

            res = {"total": paginator.count,
                   "num_pages": paginator.num_pages,
                   "current_page": page,
                   "page_size": page_size,
                   "info": info}
            return ApiResponse.success(data=res)
        else:
            return ApiResponse.http_error()

    def get_task_execute_info(request):
        if request.method == 'GET':
            id = request.GET.get("id")
            top_k = 5

            try:
                task_execute = TaskExecute.objects.get(id=id)
            except Exception:
                return ApiResponse.error(message="Task not exists.")
            dataset_from = task_execute.dataset_range.split(",")[0]
            dataset_from = datetime.datetime.fromtimestamp(int(dataset_from))
            dataset_to = task_execute.dataset_range.split(",")[1]
            dataset_to = datetime.datetime.fromtimestamp(int(dataset_to))
            if not task_execute.end_time:
                cost = '-'
            else:
                cost = (task_execute.end_time - task_execute.start_time).total_seconds()
            
            indicator_id = task_execute.template.indicator_id
            try:
                indicator = EvaluationIndicator.objects.get(id=indicator_id)
            except Exception as e:
                res = {"task_name": task_execute.task_name,
                   "execute_person": task_execute.execute_person,
                   "dataset_range": f"{dataset_from}-{dataset_to}",
                   "start_time": task_execute.start_time.strftime('%Y年%m月%d日 %H:%M:%S'),
                   "cost": cost,
                   "res": '无结果',
                   "indicator": None,
                   "dataset_type": task_execute.template.algorithm.dataset_type}
                return ApiResponse.success(data=res)
            
            indicator_json = {"indicator_name": indicator.indicator_name,
                        "indicator_format": indicator.format_json}
            if not task_execute.execute_result:
                execute_result = '无结果'
            else:
                execute_result = task_execute.execute_result
                execute_result = json.loads(execute_result)
                algorithm_type = task_execute.template.algorithm.algorithm_type.name
                execute_result = calculate_evaluation_metrics(execute_result, algorithm_type, indicator_json)

            print('execute result', execute_result)
            res = {"task_name": task_execute.task_name,
                   "execute_person": task_execute.execute_person,
                   "dataset_range": f"{dataset_from}-{dataset_to}",
                   "start_time": task_execute.start_time.strftime('%Y年%m月%d日 %H:%M:%S'),
                   "cost": cost,
                   "res": execute_result,
                   "indicator": indicator_json,
                   "dataset_type": task_execute.template.algorithm.dataset_type}
            return ApiResponse.success(data=res)
        else:
            return ApiResponse.http_error()

    def execute_task_template(request):
        # 任务模板执行
        if request.method == 'POST':
            raw_data = request.body
            data = json.loads(raw_data)

            template_id = data.get("template_id")
            task_name = data.get("task_name")
            dataset_range = data.get("dataset_range")
            execute_type = data.get("execute_type") # 立即or定时 0 or 1
            execute_type = str(execute_type)

            train_or_test = None
            try:
                task_template = TaskTemplate.objects.get(id=template_id)
                if not task_template.algorithm.container_created:
                    return ApiResponse.error(message="The algorithm container used by this template has been deleted and cannot be executed.")
                # 判断算法是否是拆分的
                if task_template.algorithm.is_split:
                    if task_template.indicator_id == None:
                        train_or_test = "train"
                    else:
                        train_or_test = "test"
            except Exception as e:
                return ApiResponse.error(message="Template not exists.")
            
            execute_status = "waiting" # waiting,running,finished,interrupted,failed
            execute_person = request.user.username
            start_time = None
            if execute_type == "0":
                start_time = timezone.now()
            elif execute_type == "1":
                start_time = int(data.get("start_time")) # 传入的是时间戳
                start_time = timezone.make_aware(timezone.datetime.fromtimestamp(start_time)) # 需要转换成timezone形式
            task_execute = TaskExecute.objects.create(
                template_id = template_id,
                task_name = task_name,
                dataset_range = dataset_range,
                execute_type = execute_type,
                execute_status = execute_status,
                execute_person = execute_person,
                create_person = execute_person,
                start_time = start_time,
                train_or_test = train_or_test
            )
            if not task_execute:
                return ApiResponse.error(message="Execute failed.")
            # 传回任务id
            return ApiResponse.success(data=task_execute.id,message="Execute successfully.")
        else:
            return ApiResponse.http_error()

    def execute_task_again(request):
        # 任务模板执行
        if request.method == 'POST':
            raw_data = request.body
            data = json.loads(raw_data)
            task_id = data.get("task_id")
            dataset_range = data.get("dataset_range")
            execute_type = data.get("execute_type")  # 立即or定时 0 or 1
            execute_task = TaskExecute.objects.get(id=task_id)
            if not execute_task:
                return ApiResponse.error(message="Task does not exist")
            if not execute_task.template.algorithm.container_created:
                return ApiResponse.error(message="The algorithm container for the task template has been deleted, cannot execute again")
            if execute_task.execute_status == 'waiting' or execute_task.execute_status == 'running':
                return ApiResponse.error(message="Task has not started or is currently running!")

            start_time = None
            if execute_type == "0":
                start_time = timezone.now()
            elif execute_type == "1":
                start_time = int(data.get("start_time"))  # 传入的是时间戳
                start_time = timezone.make_aware(timezone.datetime.fromtimestamp(start_time))  # 需要转换成timezone形式
            task_execute = TaskExecute.objects.create(
                template_id = execute_task.template_id,
                task_name = execute_task.task_name,
                dataset_range = dataset_range,
                execute_type = execute_type,
                execute_status = 'waiting',
                execute_person = request.user.username,
                create_person = execute_task.create_person,
                start_time = start_time,
                train_or_test = execute_task.train_or_test
            )
            if not task_execute:
                return ApiResponse.error(message="Execution failed!")
            return ApiResponse.success(message="Re-execution successful!")
        else:
            return ApiResponse.http_error()


    def stop_execute_task(request):
        # 中断任务的执行
        if request.method == 'POST':
            try:
                raw_data = request.body
                data = json.loads(raw_data)
                id = data.get("id") #拿到任务id，知道要中断哪一个任务
                username = request.user.username

                message = stop_task(username,id)
                
                return ApiResponse.success(message=message)
            except Exception as e:
                return ApiResponse.error(message=f"Interrupt failed:{e}")
        else:
            return ApiResponse.http_error()

# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 POST
@require_http_methods(["POST", "GET"])
class AlgorithmView(View):
    def fetch_algorithms(request):
        if request.method == 'GET':
            algorithms = Algorithm.objects.all()
            client = docker.from_env()
            # client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            res = []
            for algorithm in algorithms:
                algorithm_name = algorithm.algorithm_name
                container_status = None
                try:
                    container = client.containers.get(algorithm_name)
                    if container.status == "running":
                        container_status = True
                    else:
                        container_status =False
                    algorithm.container_status = container_status
                    algorithm.save()
                except docker.errors.APIError as e:
                    print(e)
                res.append(
                    {
                        "id": algorithm.id,
                        "algorithm_name": algorithm.algorithm_name,
                        "algorithm_type": algorithm.algorithm_type_id,
                        "container_created": algorithm.container_created,
                        "container_id": algorithm.container_id,
                        "is_split": algorithm.is_split,
                        "cpu_count": algorithm.cpu_count,
                        "mem_limit": algorithm.mem_limit,
                        "container_status": algorithm.container_status,
                    }
                )

            # 返回查询结果
            return ApiResponse.success(data=res)
        else:
            return ApiResponse.http_error()

    def import_algorithm(request):
        # 导入算法文件zip解压包，解压到djangoTemplate/xxxTemplate文件夹下
        if request.method == 'POST':
            uploaded_file = request.FILES.get('uploaded_file')
            destination_folder = os.path.join(root_path,'djangoTemplate') # 指定解压目标文件夹
            algorithm_type = request.POST.get('algorithm_type')
            algorithm_name = request.POST.get('algorithm_name').lower()
            dataset_type = request.POST.get('dataset_type')
            is_split = bool(int(request.POST.get('is_split')))
            file_name = algorithm_name+'Template'
            extracted_folder_path = os.path.join(destination_folder, file_name)
            # 创建随机数命名的临时文件夹
            random_folder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            temp_folder_path = os.path.join(destination_folder, random_folder_name)
            os.makedirs(temp_folder_path)
            try:
                # 检查算法是否已存在
                existing_algorithm = Algorithm.objects.filter(algorithm_name=algorithm_name).first()
                if existing_algorithm:
                    raise Exception("Algorithm already exists, please do not import again")

                if os.path.exists(extracted_folder_path):
                    raise Exception("Algorithm folder already exists, please do not import again")
                
                # 使用zipfile模块解压上传的文件
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_folder_path)
                
                # 检查temp_folder_path下是否存在_MACOSX文件夹
                macosx_folder = os.path.join(temp_folder_path, '__MACOSX')
                if os.path.exists(macosx_folder) and os.path.isdir(macosx_folder):
                    contents = os.listdir(temp_folder_path)
                    folder_path = os.path.join(temp_folder_path, contents[0])
                    os.rename(folder_path,extracted_folder_path)
                    shutil.rmtree(temp_folder_path)
                elif len(os.listdir(temp_folder_path)) == 1:
                    contents = os.listdir(temp_folder_path)
                    folder_path = os.path.join(temp_folder_path, contents[0])
                    os.rename(folder_path, extracted_folder_path)
                    shutil.rmtree(temp_folder_path)
                else:
                    os.rename(temp_folder_path, extracted_folder_path)

                # 创建新的Algorithm对象并保存到数据库
                algorithm=Algorithm.objects.create(
                    algorithm_name = algorithm_name,
                    algorithm_type_id = algorithm_type,
                    container_created = False,
                    is_split = is_split,
                    dataset_type = dataset_type,
                )

                return ApiResponse.success(data=algorithm.id, message=f"Algorithm imported successfully! Algorithm folder path is {os.path.join(root_path, 'djangoTemplate', file_name)}")

            except Exception as e:
                print(e)
                # 如果失败，就把temp删了
                if os.path.exists(temp_folder_path):
                    shutil.rmtree(temp_folder_path)
                return ApiResponse.error(message=f"Import algorithm failed: {e}")
        else:
            return ApiResponse.http_error()

    def delete_algorithm(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            algorithm_name = data['algorithm_name']

            file_name = algorithm_name+'Template'

            algorithm_path = os.path.join(root_path,'djangoTemplate',file_name)
            print(algorithm_path)
            
            if algorithm_name is None:
                return ApiResponse.error(message="Algorithm name not provided.")
            
            try:
                algorithm = Algorithm.objects.get(algorithm_name=algorithm_name)

                algorithm.delete()

                if os.path.exists(algorithm_path):
                    # 如果路径存在，则删除文件夹
                    shutil.rmtree(algorithm_path)
                
                return ApiResponse.success(message="Delete algorithm successfully.")

            except Exception as e:
                return ApiResponse.error(message=f"Delete algorithm failed:{e}")
        else:
            return ApiResponse.http_error()

    def start_container(request):
        # 点击部署后，进行创建容器
        if request.method == "POST":
            # 从request中获取算法名
            data = json.loads(request.body)
            algorithm_name = data['algorithm_name']
            cpu_count = data['cpu_count']
            mem_limit = data['mem_limit']
            algorithm = Algorithm.objects.get(algorithm_name=algorithm_name)

            # 使用 Docker SDK 创建 Docker 容器
            client = docker.from_env()
            folder_path = os.path.join(root_path,'djangoTemplate',f'{algorithm_name}Template')

            try:
                try:
                    image = client.images.get(algorithm_name)
                except docker.errors.ImageNotFound as e:
                    image,build_logs = client.images.build(
                        path=folder_path, tag=algorithm_name
                    )
                    print("Image build successfully:", image.tags[0])
                    
            except docker.errors.BuildError as e:
                print("Image build failed:", e)
                return ApiResponse.error(message="Image build failed.")


            try:
                try:
                    container = client.containers.get(algorithm_name)
                    if container:
                        return ApiResponse.error(data=container.id,message="Container already exists.")
                except docker.errors.NotFound:
                    container = client.containers.run(
                        image=image.tags[0],
                        name=algorithm_name,
                        detach=True,
                        cpu_count=int(cpu_count),   # 指定容器的CPU个数
                        mem_limit=mem_limit,   # 指定容器的内存上限
                        command="sh -c 'python manage.py runserver 0.0.0.0:8000'",  # 指定容器启动时要执行的命令
                        volumes={
                            folder_path: {"bind": "/code", "mode": "rw"}  # 将主机上的当前工作目录挂载到容器的 /code 目录，并设置读写权限
                        }
                    )
                    
                    while container is None or container.status != "running":
                        try:
                            container = client.containers.get(algorithm_name)
                            if container:
                                print("Container started successfully! Container ID is", container.id)
                                container_ip = container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
                                print("Container ip is:", container_ip)
                                break
                        except docker.errors.NotFound:
                            pass
                        time.sleep(1)  # 等待1秒后重新尝试获取容器对象，否则有可能会导致容器还未完全创建，ip无法获取到

                    print(container.logs())

                    dataset_path = os.path.join('djangoTemplate',f'{algorithm_name}Template','algorithm_app','experiment','{user}','origin_data/')
                    if container.status == "running":
                        algorithm.container_status = True
                    else:
                        algorithm.container_status = False
                    # 更新算法对象的属性
                    algorithm.cpu_count = cpu_count
                    algorithm.mem_limit = mem_limit
                    algorithm.container_created = True
                    algorithm.container_id = container.id 
                    algorithm.container_port = 8000
                    algorithm.container_ip = container_ip
                    if not algorithm.is_split:
                        algorithm.run_command = f'curl "http://{container_ip}:{algorithm.container_port}/modelrun?user={{}}&id={{}}"'
                    else:
                        algorithm.train_command = f'curl "http://{container_ip}:{algorithm.container_port}/modeltrain?user={{}}&id={{}}"'
                        algorithm.test_command = f'curl "http://{container_ip}:{algorithm.container_port}/modeltest?user={{}}&id={{}}"'
                    algorithm.dataset_path = dataset_path
                    algorithm.save()  # 保存更新后的算法对象到数据库
                    return ApiResponse.success(data=container.id,message="Container start successfully!")

            except docker.errors.APIError as e:
                print("Container start failed:", e)
                container = client.containers.get(algorithm_name)
                if container:
                    container.remove()
                
                return ApiResponse.error(message="Container start failed.")

        else:
            return ApiResponse.http_error()

    def delete_container(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            algorithm_name = data['algorithm_name']
            
            if algorithm_name is None:
                return ApiResponse.error(message="Algorithm name not provided.")
            
            try:
                algorithm = Algorithm.objects.get(algorithm_name=algorithm_name)

                # 删除容器后检查任务执行中，是否有关联到该算法的，有，就看它的状态是wait还是running，是wait就直接改为stop，是running就调用中断函数
                related_tasks = TaskExecute.objects.filter(template__algorithm=algorithm)
                for task in related_tasks:
                    # 如果任务状态是等待中，直接将状态设为停止
                    if task.execute_status == 'waiting':
                        task.execute_status = 'stop'
                        task.save()
                    # 如果任务状态是运行中，调用中断函数
                    elif task.execute_status == 'running':
                        stop_task(request.user.username,task.id)
                
                client = docker.from_env()
                
                # 停止并删除容器
                container = client.containers.get(algorithm_name)
                container.stop()
                container.remove()

                # 删除容器
                algorithm.cpu_count = None
                algorithm.mem_limit = None
                algorithm.container_created = False
                algorithm.container_id = None
                algorithm.container_ip = None
                algorithm.container_port = None
                algorithm.run_command = None
                algorithm.train_command = None
                algorithm.test_command = None
                algorithm.dataset_path = None
                algorithm.container_status = None

                algorithm.save()
                
                return ApiResponse.success(message="Delete container successfully.")
            except docker.errors.NotFound:
                return ApiResponse.error(message="Container not exists.")

            except Exception as e:
                return ApiResponse.error(message=f"Delete container failed:{e}")
        else:
            return ApiResponse.http_error()
    
    def fetch_algorithm_type(request):
        if request.method == 'GET':
            try:
                algorithm_types = AlgorithmType.objects.all()
                res = []
                for algorithm_type in algorithm_types:
                    res.append(
                        {
                            'id': algorithm_type.id,
                            'algorithm_type_name': algorithm_type.name
                        }
                    )
                return ApiResponse.success(data=res)

            except Exception as e:
                return ApiResponse.error(message=e)
        else:
            return ApiResponse.http_error()
    
    def restart_container(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            algorithm_name = data['algorithm_name']
            
            if algorithm_name is None:
                return ApiResponse.error(message="Algorithm name not provided.")
            
            try:
                algorithm = Algorithm.objects.get(algorithm_name=algorithm_name)
                
                client = docker.from_env()
                
                container = client.containers.get(algorithm_name)
                container.stop()

                container.start()

                algorithm.save()
                
                return ApiResponse.success(message="Container restart successfully!")
            except Exception as e:
                return ApiResponse.error(message=f"Container restart failed!{e}")
        else:
            return ApiResponse.http_error()
        
    def fetch_indicators(request):
        if request.method == 'GET':
            try:

                indicators = EvaluationIndicator.objects.all()
                res = []

                for indicator in indicators:
                    res.append(
                        {
                            'id': indicator.id,
                            'indicator_name':indicator.indicator_name,
                            'algorithm_type': indicator.algorithm_type.name,
                            'format_json':indicator.format_json,
                        }
                    )

                return ApiResponse.success(data=res,message="Evaluation metrics fetch failed!")

            except Exception as e:
                return ApiResponse.error(message=f"Evaluation metrics fetch successfully!{e}")
        else:
            return ApiResponse.http_error()
        
    def download_dataset(request):
        if request.method == 'GET':
            zip_file_path = os.path.join(root_path, 'dataset.zip')
            # 检查压缩包是否存在
            if os.path.exists(zip_file_path):
                response = FileResponse(open(zip_file_path, 'rb'))
                response['Content-Type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(zip_file_path))
                return response
            else:
                return ApiResponse.error(message="Zip not exists.")
        else:
            return ApiResponse.http_error()
    
    def export_algorithm(request):
        # 导出配置文件
        if request.method == 'GET':
            # is_split为0代表不拆分，只有run；为1代表拆分，有test和train
            is_split = request.GET.get("is_split")
            if is_split == "1":
                zip_file_path = os.path.join(root_path, 'algorithmTemplate_issplit.zip')
            elif is_split == "0":
                zip_file_path = os.path.join(root_path, 'algorithmTemplate_nosplit.zip')

            # 检查压缩包是否存在
            if os.path.exists(zip_file_path):
                response = FileResponse(open(zip_file_path, 'rb'))
                response['Content-Type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(zip_file_path))
                return response
            else:
                return ApiResponse.error(message="Zip not exists.")
        else:
            return ApiResponse.http_error()

    def get_container_log(request):
        if request.method == 'GET':
            id = request.GET.get("id")
            if not id:
                return ApiResponse.error(message="Algorithm id not provided.")
            try:
                algorithm = Algorithm.objects.get(id=id)

                if algorithm.container_created == False:
                    return ApiResponse.error(message="Container not deployed, can't query logs.")

                algorithm_name = algorithm.algorithm_name

                client = docker.from_env()
                
                container = client.containers.get(algorithm_name)

                log_file_path = os.path.join(root_path,'djangoTemplate','log.txt')

                # 获取容器日志并写入到日志文件
                log = ''
                log = container.logs().decode('utf-8')
                
            except Exception as e:
                return ApiResponse.error(message=f"Query log failed:{e}")

            return ApiResponse.success(data=log)
        else:
            return ApiResponse.http_error()
        
    def train_algorithm(request):
        if request.method == 'GET':
            algorithm_id = request.GET.get("algorithm_id")
            task_name = request.GET.get("task_name")
            dataset_range = request.GET.get("dataset_range")
            execute_type = str(request.GET.get("execute_type")) # 立即or定时 0 or 1

            algorithm = Algorithm.objects.get(id=algorithm_id)
            if not algorithm.container_status:
                return ApiResponse.error(message="The algorithm container for this template has not been deployed and cannot be executed.")
            execute_status = "waiting" # waiting,running,finished,interrupted,failed
            execute_person = request.user.username
            start_time = None
            if execute_type == "0":
                start_time = timezone.now()
            elif execute_type == "1":
                start_time = int(request.GET.get("start_time")) # 传入的是时间戳
                start_time = timezone.make_aware(timezone.datetime.fromtimestamp(start_time)) # 需要转换成timezone形式
            
            algorithm_name = algorithm.algorithm_name + '_trainTemplate'
            task_template = TaskTemplate.objects.filter(template_name=algorithm_name).first()
            if not task_template:
                task_template = TaskTemplate.objects.create(template_name=algorithm_name,
                                                        algorithm_id=algorithm_id,
                                                        create_person=execute_person,
                                                        is_evaluate='False')
            task_execute = TaskExecute.objects.create(
                template_id = task_template.id,
                task_name = task_name,
                dataset_range = dataset_range,
                execute_type = execute_type,
                execute_status = execute_status,
                execute_person = execute_person,
                create_person = execute_person,
                start_time = start_time,
                train_or_test = 'train'
            )
            # 传回任务id
            return ApiResponse.success(data=task_execute.id,message="Execute successfully.")
        else:
            return ApiResponse.http_error()


