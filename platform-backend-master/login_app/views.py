import datetime
import hashlib
import json
import time

import jwt
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from platform_backend import ApiResponse
from platform_backend import settings
from .models import User, Role, RelationUserRole, EmailVerifyRecord
from .utils import email_send


# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 POST
@require_http_methods(["POST", "GET"])
class LoginView(View):
    def query_login_by_username(request):
        if request.method == "POST":
            # 获取原始请求体数据
            raw_data = request.body
            # 解析Json数据
            data = json.loads(raw_data)
            username = data.get("username")  # 获取用户名
            password = data.get("password")  # 获取密码
            try:
                md5_password = password_encode(password)
                user = User.objects.get(username=username)
                if user.password == md5_password:
                    token = jwt.encode(
                        {
                            "exp": timezone.datetime.utcnow()
                            + timezone.timedelta(days=1),
                            "iat": timezone.datetime.utcnow(),
                            "data": {"id": user.id},
                        },
                        settings.SECRET_KEY,
                        algorithm="HS256",
                    )  # 用户名和密码验证成功, 生成token
                    return ApiResponse.success(data={"token": token.decode("utf-8"),
                                                     "username": username,
                                                    'email': User.email})
                else:
                    return ApiResponse.error('Wrong Password!')  # 密码验证失败
            except Exception as e:
                return ApiResponse.error(f"error: {str(e)}")
        else:
            return ApiResponse.http_error()


    def query_login_by_email(request):
        if request.method == "POST":
            # 获取原始请求体数据
            raw_data = request.body
            # 解析Json数据
            data = json.loads(raw_data)
            email = data.get("email")  # 获取用户名
            password = data.get("password")  # 获取密码
            try:
                md5_password = password_encode(password)
                user = User.objects.get(email=email)
                if user.password == md5_password:
                    token = jwt.encode(
                        {
                            "exp": timezone.datetime.utcnow()
                            + timezone.timedelta(days=1),
                            "iat": timezone.datetime.utcnow(),
                            "data": {"id": user.id},
                        },
                        settings.SECRET_KEY,
                        algorithm="HS256",
                    )  # 用户名和密码验证成功, 生成token
                    return ApiResponse.success(data={"token": token.decode("utf-8"),
                                                     "username": user.username,
                                                     'email': User.email})
                else:
                    return ApiResponse.error('Wrong Password!')  # 密码验证失败
            except Exception as e:
                return ApiResponse.error(f"error: {str(e)}")
        else:
            return ApiResponse.http_error()

# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 POST
@require_http_methods(["POST", "GET"])
class RoleView(View):
    def get_user_level(user_id):
        role_ids = RelationUserRole.objects.filter(user_id=user_id).values_list(
            "role_id"
        )
        role_ids = list(role_ids)  # 获取当前用户所拥有角色id
        level = 0x7FFFFFFF  # 要获取最小的level 预先设为MAX_INT
        # 获取最小的角色level
        for role_id in role_ids:
            role_level = Role.objects.filter(id=role_id[0]).first().level
            level = min(level, role_level)
        return level

    def query_role_list(request):
        """
        获取用户可修改角色列表，获取大于当前用户最高角色等级(>=level)对应的角色列表
        params:
            params1: request
        method:
            method1: get
        return:
           {{
            level: 1,
            name: '管理员',
            code: 'admin',
            desc: '可管理除管理员外其他角色权限',
            createTime: timestamp(11位), // 需要去除后三位
            lastEditTime: timestamp(11位), // 需要去除后三位
            authorityListDict: {
            Fault-injection: literal[true, false], // 故障注入授权
            DataMonitor: literal[true, false],  // 运维数据监控授权
            Detection: literal[true, false], // 故障检测授权
            Diagnosis: literal[true, false], // 故障诊断授权
            Manage: literal[true, false], // 用户管理
            RecordShow: literal[true, false] // 系统日志}
           },...}
        """
        if request.method == "GET":
            try:
                user_id = request.user.id  # 获取当前用户的id
                level = RoleView.get_user_level(user_id)  # 获取当前用户最高角色等级
                if level == 0x7FFFFFF:
                    return ApiResponse.success(data={})
                roles = Role.objects.filter(level__gte=level).all()  # 获取所有的结果
                res = []
                for role in roles:
                    res.append(
                        {
                            "level": role.level,
                            "name": role.name,
                            "code": role.code,
                            "desc": role.description,
                            "createTime": str(role.create_time.replace(tzinfo=None)),
                            "lastEditTime": str(
                                role.last_edit_time.replace(tzinfo=None)
                            ),
                            "authorityListDict": {
                                "Fault-injection": role.fault_injection,
                                "DataMonitor": role.data_monitor,
                                "Detection": role.detection,
                                "Diagnosis": role.diagnosis,
                                "Manage": role.manage,
                                "RecordShow": role.RecordShow,
                            },
                        }
                    )
                return ApiResponse.success(data=res)
            except Exception as e:
                return ApiResponse.error(f'error:{str(e)}')
        else:
            return ApiResponse.http_error()

    def add_role(request):
        """
        添加角色,该角色等级为当前用户最高角色的等级+1
        params:
            params1: request
            {
            level: -1, // 需要后端修改重新赋值level
            name: '管理员',
            code: 'admin', // 不可重名
            desc: '可管理除管理员外其他角色权限',
            createTime: timestamp(11位), // 需要去除后三位
            lastEditTime: timestamp(11位), // 需要去除后三位
            authorityListDict: {
              Fault-injection: [true,false], // 故障注入授权
              DataMonitor: [true,false], // 运维数据监控授权
              Detection: [true,false], // 故障检测授权
              Diagnosis: [true,false], // 故障诊断授权
              Manage: [true,false], // 用户管理
              RecordShow: [true,false] // 系统日志 }
            }
        method:
            method1: post
        return:
            { msg: "success"}
        """
        if request.method == "POST":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                user_id = request.user.id  # 获取当前用户的id
                level = RoleView.get_user_level(user_id)  # 获取当前用户最高角色等级
                data["createTime"] = time.localtime(
                    int(str(data["createTime"])[:-3])
                )  # 转换成localtime
                data["createTime"] = time.strftime(
                    "%Y-%m-%d %H:%M:%S", data["createTime"]
                )
                data["lastEditTime"] = time.localtime(
                    int(str(data["lastEditTime"])[:-3])
                )  # 转换成localtime
                data["lastEditTime"] = time.strftime(
                    "%Y-%m-%d %H:%M:%S", data["lastEditTime"]
                )
                if level == 0x7FFFFFFF:
                    data["level"] = 1
                else:
                    data["level"] = level + 1
                if Role.objects.filter(code=data["code"]).exists():
                    return ApiResponse.error('Role Already Exists!')
                else:
                    Role.objects.create(
                        level=data["level"],
                        name=data["name"],
                        code=data["code"],
                        description=data["desc"],
                        create_time=data["createTime"],
                        last_edit_time=data["lastEditTime"],
                        fault_injection=data["authorityListDict"]["Fault-injection"],
                        data_monitor=data["authorityListDict"]["DataMonitor"],
                        detection=data["authorityListDict"]["Detection"],
                        diagnosis=data["authorityListDict"]["Diagnosis"],
                        manage=data["authorityListDict"]["Manage"],
                        RecordShow=data["authorityListDict"]["RecordShow"],
                    )
                    return ApiResponse.success()
            except Exception as e:
                return ApiResponse.error(f'error: {str(e)}')
        else:
            return ApiResponse.http_error()

    def modify_role_auth(request):
        """
        修改角色权限
        params:
            params1: request
            {
            level: -1,
            name: '管理员',
            code: 'admin', // 不可重名
            desc: '可管理除管理员外其他角色权限',
            createTime: timestamp(11位), // 需要去除后三位
            lastEditTime: timestamp(11位), // 需要去除后三位
            authorityListDict: {
              Fault-injection: [true,false], // 故障注入授权
              DataMonitor: [true,false], // 运维数据监控授权
              Detection: [true,false], // 故障检测授权
              Diagnosis: [true,false], // 故障诊断授权
              Manage: [true,false], // 用户管理
              RecordShow: [true,false],} // 系统日志
            }
        method:
            method1: put
        return:
            { msg: "success"}
        """
        if request.method == "PUT":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                code = data["code"]
                if Role.objects.filter(code=code).exists():
                    role = Role.objects.filter(code=code).first()
                    role.name = data["name"]
                    role.description = data["desc"]
                    role.fault_injection = data["authorityListDict"]["Fault-injection"]
                    role.data_monitor = data["authorityListDict"]["DataMonitor"]
                    role.detection = data["authorityListDict"]["Detection"]
                    role.diagnosis = data["authorityListDict"]["Diagnosis"]
                    role.manage = data["authorityListDict"]["Manage"]
                    role.RecordShow = data["authorityListDict"]["RecordShow"]
                    role.save()
                    return ApiResponse.success()
                else:
                    return ApiResponse.error('Role Not Exists!')
            except Exception as e:
                return ApiResponse.error(f'error: {str(e)}')
        else:
            return ApiResponse.http_error()

    def delete_role(request):
        """
        删除角色
        params:
            params1: request
            {
            level: 1,
            name: '管理员',
            code: 'admin',
            desc: '可管理除管理员外其他角色权限',
            createTime: timestamp(11位), // 需要去除后三位
            lastEditTime: timestamp(11位), // 需要去除后三位
            authorityListDict: {
              Fault-injection: [true,false], // 故障注入授权
              DataMonitor: [true,false], // 运维数据监控授权
              Detection: [true,false], // 故障检测授权
              Diagnosis: [true,false], // 故障诊断授权
              Manage: [true,false], // 用户管理
              RecordShow: [true,false] // 系统日志
              }
            }
        method:
            method1: delete
        return:
            { msg: "success"}
        """
        if request.method == "DELETE":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                code = data["code"]
                if Role.objects.filter(code=code).exists():
                    Role.objects.filter(code=code).delete()
                    return ApiResponse.success()
                else:
                    return ApiResponse.error('Role Not Exists!')

            except Exception as e:
                return ApiResponse.error(f'error: {str(e)}')
        else:
            return ApiResponse.http_error()

def verify_email_code(email, code, send_type):
    email_object = EmailVerifyRecord.objects.filter(email=email, send_type=send_type).order_by('-send_time').first()
    if (not email_object
            or datetime.datetime.now(datetime.timezone.utc) - email_object.send_time > datetime.timedelta(minutes=settings.EMAIL_TIMEOUT)
            or code != email_object.code):
        return False
    return True

def password_encode(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 POST
@require_http_methods(["POST", "GET"])
class UserView(View):

    def register(request):
        if request.method == "POST":
            raw_data = request.body  # 获取原始请求体数据
            data = json.loads(raw_data)  # 解析Json数据
            email = data["email"]
            code = data["code"]
            username = data["username"]
            password = data["password"]
            password = password_encode(password)
            # 验证邮箱是否注册
            if User.objects.filter(email=email).exists():
                return ApiResponse.error(message="This email has already been registered!")
            # 验证用户名是否注册
            if User.objects.filter(username=username).exists():
                return ApiResponse.error(message="This username has already been registered!")
            # 验证验证码有效性
            if not verify_email_code(email, code, "register"):
                return ApiResponse.error(message="Verification code validation failed!")
            # 验证成功，保存用户
            User.objects.create(username=username, password=password, email=email)
            return ApiResponse.success(message="Registration successful!")
        else:
            return ApiResponse.http_error()

    def retrieve(request):
        if request.method == "POST":
            raw_data = request.body  # Get the raw request body data
            data = json.loads(raw_data)  # Parse JSON data
            email = data["email"]
            code = data["code"]
            password = data["password"]
            password = password_encode(password)
            # Verify whether the email is registered
            if not User.objects.filter(email=email).exists():
                return ApiResponse.error(message="This email is not registered yet!")
            # Verify the validity of the verification code
            if not verify_email_code(email, code, "retrieve"):
                return ApiResponse.error(message="Verification code validation failed!")
            # Verification successful, save user
            user = User.objects.filter(email=email).first()
            user.password = password
            user.save()
            return ApiResponse.success(message="Password changed successfully!")
        else:
            return ApiResponse.http_error()

    def send_email(request):
        if request.method == "POST":
            raw_data = request.body  # Get the raw request body data
            data = json.loads(raw_data)  # Parse JSON data
            email = data["email"]
            send_type = data["send_type"]
            if not send_type or (send_type != "register" and send_type != "retrieve"):
                send_type = "register"
            if send_type == "register":
                # Verify whether the email is registered, for registration type the email should not be registered yet
                if User.objects.filter(email=email).exists():
                    return ApiResponse.error(message="This email has already been registered!")
            if send_type == "retrieve":
                # Verify whether the email is registered, for retrieval type the email should already be registered
                if not User.objects.filter(email=email).exists():
                    return ApiResponse.error(message="This email is not registered yet!")
            if email_send.send_code_email(email, send_type=send_type):
                return ApiResponse.success(message="Sent successfully!")
            return ApiResponse.error(message="Failed to send!")
        else:
            return ApiResponse.http_error()

    def add_user(request):
        """
        添加·对应用户
        params：
            param1： request
            {
            id: 0,
            name: '张三',
            phone: '13478414545',
            email: '',
            password: '',
            department: '管理部门',
            createTime: timestamp(11位), // 需要去除后三位
            lastEditTime: timestamp(11位), // 需要去除后三位
            description: '',
            ownRoles: ['user']
            }
        method：
            method1： post
        return：
            {msg: "success"}
        """
        if request.method == "POST":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                # password md5 hash
                data["password"] = password_encode(data["password"])
                if data["id"] is not None and data["id"] != "" and User.objects.filter(id=data["id"]).exists():
                    return ApiResponse.error('ID Already Exists')
                if User.objects.filter(username=data["name"]).exists():
                    return ApiResponse.error('Username Already Exists')
                user = User.objects.create(
                    username=data["name"],
                    password=data["password"],
                    phone=data["phone"],
                    email=data["email"],
                    department=data["department"],
                    description=data["description"],
                )

                for code in data["ownRoles"]:
                    role = Role.objects.filter(code=code).first()
                    if role is not None:
                        RelationUserRole.objects.create(
                            user_id=user.id, role_id=role.id
                        )
                return ApiResponse.success(data="新建用户成功！")
            except Exception as e:
                return ApiResponse.error(f'error: {str(e)}')
        else:
            return ApiResponse.http_error()

    def modify_user(request):
        """
        修改·对应用户
        params：
            param1： request
            {
            id: 0,
            name: '张三',
            phone: '13478414545',
            email: '',
            password: '',
            department: '管理部门',
            createTime: timestamp(11位), // 需要去除后三位
            lastEditTime: timestamp(11位), // 需要去除后三位
            description: '',
            ownRoles: ['user']
            }
        method：
            method1：put
        return：
            {msg: "success"}
        """
        if request.method == "PUT":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                if data["password"] is not None and data["password"] != "":
                    md5 = hashlib.md5()
                    md5.update(data["password"].encode())
                    data["password"] = md5.hexdigest()
                if not User.objects.filter(id=data["id"]).exists():
                    return ApiResponse.error("User Doesn't Exist")
                user = User.objects.filter(id=data["id"]).first()
                user.id = data["id"]
                user.username = data["name"]
                user.phone = data["phone"]
                user.email = data["email"]
                user.department = data["department"]
                user.description = data["description"]
                RelationUserRole.objects.filter(user_id=user.id).delete()
                for code in data["ownRoles"]:
                    role = Role.objects.filter(code=code).first()
                    if role is not None:
                        RelationUserRole.objects.create(
                            user_id=user.id, role_id=role.id
                        )
                if data["password"] is not None and data["password"] != "" and user.password != data["password"]:
                    user.password = data["password"]
                user.save()
                return ApiResponse.success(data="修改用户成功！")
            except Exception as e:
                return ApiResponse.error(f'error: {e}')
        else:
            return ApiResponse.http_error()

    def delete_user(request):
        """
        删除·对应用户
        params:
            param1: request
            {id: string}
            {id: 0}
        method:
            method1: delete
        return:
            {msg: "success"}
        """
        if request.method == "DELETE":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                del_id = data["id"]
                if User.objects.filter(id=del_id).exists():
                    User.objects.filter(id=del_id).delete()
                    return ApiResponse.success(data="用户删除成功！")
                else:
                    return ApiResponse.error('User Not Exists!')
            except Exception as e:
                return ApiResponse.error(f'error: {str(e)}')
        else:
            return ApiResponse.http_error()

    def delete_user_by_batch(request):
        """
        批量·删除·对应用户
        params:
            param1: request
            [Number]
            [0,1,2]
        method:
            method1: delete
        return:
            {msg: "success"}
        """
        if request.method == "DELETE":
            try:
                raw_data = request.body  # 获取原始请求体数据
                data = json.loads(raw_data)  # 解析Json数据
                for del_id in data:
                    if not User.objects.filter(id=del_id).exists():
                        return ApiResponse.error(f'id: {del_id} User Not Exists!')
                for del_id in data:
                    User.objects.filter(id=del_id).delete()
                return ApiResponse.success(data="用户删除成功！")
            except Exception as e:
                return ApiResponse.error(f'error: {str(e)}')
        else:
            return ApiResponse.http_error()
