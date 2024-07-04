from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from login_app.models import EmailVerifyRecord  # 邮箱验证model
from platform_backend import settings    # setting.py添加的的配置信息

import datetime


# 生成随机字符串
def random_str(randomlength=6):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送电子邮件
def send_code_email(email, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    if send_type != "register" and send_type != "retrieve":
        return False
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = "注册激活"
    if send_type == "retrieve":
        email_title = "找回密码"
    email_body = f"您的邮箱注册验证码为：{code}, 该验证码有效时间为{settings.EMAIL_TIMEOUT}分钟，请及时进行验证。"
    # 发送邮件
    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    if not send_status:
        return False
    return True
