from django.db import models

# Create your models here.
class AlgorithmType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Algorithm(models.Model):
    id = models.AutoField(primary_key=True)
    algorithm_name = models.CharField(max_length=100)
    algorithm_type = models.ForeignKey(AlgorithmType, on_delete=models.CASCADE, null=True, blank=False)
    indicator_id = models.CharField(max_length=100, null=True)
    cpu_count = models.CharField(max_length=100, null=True)
    mem_limit = models.CharField(max_length=100, null=True)
    container_created = models.BooleanField()
    container_status = models.BooleanField(null=True)
    container_id = models.CharField(max_length=100, null=True)
    container_port = models.CharField(max_length=100, null=True)
    container_ip = models.CharField(max_length=100, null=True)
    dataset_path = models.CharField(max_length=300, null=True)
    is_split = models.BooleanField()
    run_command = models.CharField(max_length=100, null=True)
    train_command = models.CharField(max_length=100, null=True)
    test_command = models.CharField(max_length=100, null=True)
    dataset_type = models.CharField(max_length=100, null=True)

class TaskTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=100)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, null=True, blank=False)
    indicator_id = models.CharField(max_length=100, null=True)
    create_person = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_evaluate = models.CharField(max_length=100, null=True)
    record_id = models.CharField(max_length=100, null=True)

class EvaluationIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    algorithm_type = models.ForeignKey(AlgorithmType, on_delete=models.CASCADE, null=True, blank=False)
    indicator_name = models.CharField(max_length=100,null=True)
    format_json = models.TextField(null=True)

class TaskExecute(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100, null=True)
    template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, null=True, blank=False)
    dataset_range = models.CharField(max_length=100, null=True)
    execute_type = models.IntegerField()
    execute_status = models.CharField(max_length=100, null=True)
    pid = models.CharField(max_length=100, null=True)
    container_pid = models.CharField(max_length=100, null=True)
    execute_person = models.CharField(max_length=100, null=True)
    execute_result = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    create_person = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    train_or_test = models.CharField(max_length=100, null=True)
