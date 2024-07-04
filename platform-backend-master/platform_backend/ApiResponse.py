# -*- coding:utf-8 -*-

from django.http import JsonResponse


class ApiResponse:
    success = 0
    error = 1


def success(data=None, code=ApiResponse.success, message='success'):
    return JsonResponse({'data': data, 'code': code, 'message': message}, status=200)


def error(message='', data=None, code=ApiResponse.error):
    return JsonResponse({'data': data, 'code': code, 'message': message}, status=500)


def http_error():
    return JsonResponse({'data': None, 'code': ApiResponse.error, 'message': 'Invalid API request method.'}, status=400)



