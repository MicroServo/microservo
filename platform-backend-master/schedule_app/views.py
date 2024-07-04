from django.shortcuts import render
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from schedule_app.schedule import delete_indices
from algorithm_app.task import execute_timed_task
from chaosmesh_app.chaos import execute_experiment_chaos, delete_experiment_chaos
from leaderboard_app.task import execute_dataset_collect_task
import pytz
# Create your views here.

try:
    print('调度器启动')
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(delete_indices, 'cron', id='logstash', hour=0, minute=30, replace_existing=True, timezone=pytz.timezone('Asia/Shanghai'), jobstore="default")
    scheduler.add_job(execute_timed_task, 'interval', id='timedtask', seconds=60, replace_existing=True, max_instances=100)
    scheduler.add_job(execute_dataset_collect_task, 'interval', id='datasettask', seconds=60, replace_existing=True, max_instances=100)
    scheduler.add_job(execute_experiment_chaos, 'interval', id='executeexperiment', seconds=60, replace_existing=True, max_instances=100)
    # scheduler.add_job(delete_experiment_chaos, 'cron', id='deleteexperiment', hour=20, minute=5, replace_existing=True, timezone=pytz.timezone('Asia/Shanghai'), jobstore="default")

    register_events(scheduler)
    scheduler.start()
except:
    print('定时任务执行失败')

@csrf_exempt
class ScheduleView(View):
    def run_schedule(request):
        pass