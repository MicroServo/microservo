from django.db import models
import binascii
import os
from login_app.models import User

# Create your models here.


class ApiKeyToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True, verbose_name='key')
    user = models.ForeignKey('login_app.User', on_delete=models.CASCADE, null=False, blank=False)
    is_active = models.BooleanField(default=True, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    lastGetTime = models.DateTimeField(blank=True, auto_now=True, null=True, verbose_name='最近查询时间')
    countTimes = models.IntegerField(blank=True, default=0, verbose_name='key使用次数')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKeyToken, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()
