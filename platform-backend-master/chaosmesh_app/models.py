from django.db import models

# Create your models here.

class Fault(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True)
    inject_type = models.CharField(max_length=100,null=True)
    fault_type = models.CharField(max_length=255,null=True)
    spec = models.CharField(max_length=10000,null=True)
    schedule = models.CharField(max_length=100,null=True)
    create_time = models.DateTimeField(auto_now_add=True,null=True)