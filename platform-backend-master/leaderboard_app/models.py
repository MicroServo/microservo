from django.db import models
from algorithm_app.models import Algorithm, EvaluationIndicator, AlgorithmType

# Create your models here.
class LeaderboardOverall(models.Model):
    id = models.AutoField(primary_key=True)
    algorithm_type = models.ForeignKey(AlgorithmType, on_delete=models.CASCADE, null=False, blank=False)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, null=False, blank=False)
    evaluation_metric = models.ForeignKey(EvaluationIndicator, on_delete=models.CASCADE, null=False, blank=False)
    gold = models.IntegerField(null=True)
    silver = models.IntegerField(null=True)
    copper = models.IntegerField(null=True)
    strawberry = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

class LeaderboardDataset(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_name = models.CharField(max_length=255, null=True)
    dataset_path = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    start_time = models.CharField(max_length=255, null=True)
    end_time = models.CharField(max_length=255, null=True)
    pid = models.CharField(max_length=255, null=True)
    create_person = models.CharField(max_length=255, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

class LeaderboardRecord(models.Model):
    id = models.AutoField(primary_key=True)
    record_name = models.CharField(max_length=100, null=True)
    algorithm_type = models.ForeignKey(AlgorithmType, on_delete=models.CASCADE, null=False, blank=False)
    dataset = models.ForeignKey(LeaderboardDataset, on_delete=models.CASCADE, null=True)
    algorithms = models.CharField(max_length=100, null=True)  # 保存算法列表和配置
    evaluation_metrics = models.CharField(max_length=100, null=True)  # 保存评估指标
    create_person = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True)  # 保存每个算法的评估结果