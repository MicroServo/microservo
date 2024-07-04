"""platform_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from algorithm_app.views import TaskTemplateView
from backdoor_app.views import BackdoorView
from login_app.views import LoginView, UserView,RoleView
from monitor_app.views import MonitorView
from chaosmesh_app.views import ChaosMeshView
from algorithm_app.views import TaskTemplateView,AlgorithmView
from schedule_app.views import ScheduleView
from leaderboard_app.views import LeaderboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginByUsername', LoginView.query_login_by_username, name='login'),
    path('loginByEmail', LoginView.query_login_by_email, name='login'),
    path('register', UserView.register, name='register'),
    path('retrieve', UserView.retrieve, name='retrieve'),
    path('sendEmail', UserView.send_email, name='sendEmail'),

    # path('role/query', RoleView.query_role_list, name="queryrole"),
    # path('role/add', RoleView.add_role, name="addrole"),
    # path('role/modify', RoleView.modify_role_auth, name="modifyrole"),
    # path('role/delete', RoleView.delete_role, name="deleterole"),
    # path('role/queryauth', RoleView.query_auth_able_list, name="queryauthrole"),
    # path('user/query', UserView.query_user_list, name="queryuser"),
    # path('user/add', UserView.add_user, name="adduser"),
    # path('user/delete', UserView.delete_user, name="deleteuser"),
    # path('user/modify', UserView.modify_user, name="modifyuser"),
    # path('user/deletebatch', UserView.delete_user_by_batch, name="deleteuserbatch"),
    # path('user/queryauthority', UserView.query_user_authority, name="queryauthority"),


    path('backdoor/generateApiKey', BackdoorView.generate_api_key, name='backdoor/generateApiKey'),
    path('log', MonitorView.query_log_data, name='log'),
    path('logextract', MonitorView.extract_log, name='logextract'),
    path('lognum', MonitorView.query_log_num, name='lognum'),
    path('trace', MonitorView.query_trace_data, name='trace'),
    path('traceid', MonitorView.query_trace_byId, name='traceid'),
    path('traceextract', MonitorView.extract_trace, name='traceextract'),
    path('metric', MonitorView.query_prometheus_data, name='prometheus'),
    path('metricexport', MonitorView.export_metric_data, name='prometheusexport'),
    path('metricname', MonitorView.query_metric_name, name='prometheusname'),
    path('podlist', MonitorView.get_pod_list, name='getpodlist'),
    path('getTaskTemplateList', TaskTemplateView.get_task_template_list, name='get_task_template_list'),
    path('chaosmesh/get', ChaosMeshView.create_ground_truth, name='chaosmesh/get'),
    path('chaosmesh/inject', ChaosMeshView.inject_fault, name='chaomesh/inject'),
    path('chaosmesh/delete', ChaosMeshView.delete_injection, name='chaomesh/delete'),
    path('chaosmesh/getfuture', ChaosMeshView.get_future_injection, name='chaosmesh/getfuture'),
    path('chaosmesh/fetch', ChaosMeshView.fetch_injection, name='chaosmesh/fetch'),
    path('chaosmesh/groundtruthextract', ChaosMeshView.extract_ground_truth, name='chaosmesh/groundtruthextract'),
    path('getAlgorithmByType', TaskTemplateView.get_algorithm_by_type, name='get_algorithm_by_type'),
    path('getIndicatorByAlgorithmType', TaskTemplateView.get_indicator_by_algorithm_type, name='get_indicators_by_algorithm_type'),
    path('taskTemplateCreate', TaskTemplateView.task_template_create, name='task_template_create'),
    path('executeTaskTemplate', TaskTemplateView.execute_task_template, name='execute_task_template'),
    path('executeTaskAgain', TaskTemplateView.execute_task_again, name='execute_task_again'),
    path('getTaskExecuteInfo', TaskTemplateView.get_task_execute_info, name='get_task_execute_info'),
    path('getTaskExecuteList', TaskTemplateView.get_task_execute_list, name='get_task_execute_list'),
    path('deleteExecuteTask', TaskTemplateView.delete_execute_task, name='delete_execute_task'),
    path('stopExecuteTask', TaskTemplateView.stop_execute_task, name='stop_execute_task'),
    path('deleteTaskTemplate', TaskTemplateView.delete_task_template, name='delete_task_template'),
    path('algorithm/fetch', AlgorithmView.fetch_algorithms, name='fetch_algorithms'),
    path('algorithm/import', AlgorithmView.import_algorithm, name='import_algorithm'),
    path('algorithm/delete', AlgorithmView.delete_algorithm, name='delete_algorithm'),
    path('algorithm/download', AlgorithmView.download_dataset, name='download_dataset'),
    path('algorithm/export', AlgorithmView.export_algorithm, name='export_algorithm'),
    path('algorithm/fetchalgorithmtype', AlgorithmView.fetch_algorithm_type, name='fetch_algorithm_type'),
    path('algorithm/trainalgorithm', AlgorithmView.train_algorithm, name='train_algorithm'),
    path('container/delete', AlgorithmView.delete_container, name='delete_container'),
    path('container/start', AlgorithmView.start_container, name='start_container'),
    path('container/restart', AlgorithmView.restart_container, name='stop_container'),
    path('indicators/fetch', AlgorithmView.fetch_indicators, name='fetch_indicators'),
    path('container/getContainerLog', AlgorithmView.get_container_log, name='getContainerLog'),
    path('leaderboard/getallmedals', LeaderboardView.get_all_medals, name='get_all_medals'),
    path('leaderboard/getalgorithms', LeaderboardView.get_algorithms, name='get_algorithms'),
    path('leaderboard/getallrecords', LeaderboardView.get_all_records, name='get_all_records'),
    path('leaderboard/createrecord', LeaderboardView.create_record, name='create_record'),
    path('leaderboard/addnewalgorithm', LeaderboardView.add_new_algorithm, name='add_new_algorithm'),
    path('leaderboard/queryrecorddata', LeaderboardView.query_record_data, name='query_record_data'),
    path('leaderboard/reevaluation', LeaderboardView.re_evaluation, name='re_evaluation'),
    path('leaderboard/createdataset', LeaderboardView.create_dataset, name='create_dataset'),
    path('leaderboard/querydataset', LeaderboardView.query_dataset, name='query_dataset')
]
