from django.db import models


#  Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 上次修改时间
    department = models.CharField(max_length=100)
    description = models.TextField()


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField()  # 权限等级
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 上次修改时间
    fault_injection = models.BooleanField()  # 故障注入授权
    data_monitor = models.BooleanField()  # 运维数据监控授权
    detection = models.BooleanField()  # 故障检测授权
    diagnosis = models.BooleanField()  # 故障诊断授权
    manage = models.BooleanField()  # 用户管理
    RecordShow = models.BooleanField()  # 系统日志


class RelationUserRole(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=False, blank=False)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=False, blank=False)


class EmailVerifyRecord(models.Model):
    id = models.AutoField(primary_key=True)
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)
