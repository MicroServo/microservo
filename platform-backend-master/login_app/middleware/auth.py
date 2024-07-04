from django.utils.deprecation import MiddlewareMixin

from backdoor_app.models import ApiKeyToken
from login_app.models import User
from platform_backend import settings
from platform_backend import ApiResponse
import jwt


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        if (request.path_info == "/loginByUsername"
                or request.path_info == "/loginByEmail"
                or request.path_info == "/register"
                or request.path_info == "/retrieve"
                or request.path_info == "/sendEmail"
                or request.path_info.startswith("/backdoor")):
            return
        try:
            auth = request.META.get("HTTP_AUTHORIZATION").split(' ')
        except AttributeError:
            return ApiResponse.error(message="No authenticate header")
        if auth[0].lower() == 'token':
            try:
                dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
                id = dict.get('data').get('id')
                user_object = User.objects.get(id=id)
                if not user_object:
                    return ApiResponse.error(message="User Didn't Exist!")
                request.user = user_object
            except jwt.ExpiredSignatureError:
                return ApiResponse.error(message="Token expired")
            except jwt.InvalidTokenError:
                return ApiResponse.error(message="Invalid token")
            except Exception as e:
                return ApiResponse.error(message=str(e))
        elif auth[0].lower() == 'apikey':
            try:
                api_key = auth[1]
                api_key_object = ApiKeyToken.objects.get(key=api_key)
                if not api_key_object:
                    return ApiResponse.error(message="Api Key Didn't Exist!")
                if not api_key_object.is_active:
                    return ApiResponse.error(message="Api Key expired.")
                api_key_object.countTimes = api_key_object.countTimes + 1
                api_key_object.save()
                request.user = api_key_object.user
            except Exception as e:
                return ApiResponse.error(message=str(e))
        else:
            return ApiResponse.error(message="Not support auth type")



