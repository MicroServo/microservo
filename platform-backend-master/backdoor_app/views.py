from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from backdoor_app.models import ApiKeyToken
from platform_backend import ApiResponse
from login_app.models import User


# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 POST
@require_http_methods(["POST", "GET"])
class BackdoorView(View):
    def generate_api_key(request):
        # 获取原始请求体数据
        if request.method == 'GET':
            try:
                username = request.GET.get("username")
                if not User.objects.filter(username=username).exists():
                    return ApiResponse.error(message="user is not exist.")
                user = User.objects.filter(username=username).first()
                api_key_token = ApiKeyToken()
                api_key_token.user_id = user.id
                api_key_token.save()
                return ApiResponse.success(data=api_key_token.key)
            except Exception as e:
                return ApiResponse.error(message=str(e))
        else:
            return ApiResponse.http_error()
