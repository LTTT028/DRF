from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from demo01.models import User
from demo01.serializers import UserSerializer, UserDeSerializer


# 函数视图
@csrf_exempt
def user(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        print(username)
        print('GET 查询')
        return HttpResponse('GET ok')
    if request.method == 'POST':
        print('POST 新增')
        return HttpResponse('POST ok')
    if request.method == 'PUT':
        print('PUT 更改')
        return HttpResponse('PUT ok')
    if request.method == 'DELETE':
        print('DELETE 删除')
        return HttpResponse('DELETE ok')


# 类视图
@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id:
            user_val = User.objects.filter(pk=user_id).values('username', 'password', 'gender').first()
            if user_val:
                return JsonResponse({
                    'status': 200,
                    'message': '查询单个用户成功',
                    'result': user_val,
                })
            return JsonResponse({
                'status': 400,
                'message': '查询失败',
            })
        else:
            user_val = User.objects.all().values('username', 'password', 'gender')
            if user_val:
                return JsonResponse({
                    'status': 200,
                    'message': '查询所有用户成功',
                    'result': list(user_val),
                })
            return JsonResponse({
                'status': 400,
                'message': '查询失败',
            })

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                'status': 200,
                'message': "添加成功",
                'result': {'username': user_obj.username, 'gender': user_obj.gender},
            })
        except:
            return JsonResponse({
                'status': 400,
                'message': "添加失败",
            })

    def put(self, request, *args, **kwargs):
        print('PUT 更改')
        return HttpResponse('PUT ok')

    def delete(self, request, *args, **kwargs):
        print('DELETE 删除')
        return HttpResponse('DELETE ok')


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id:
            user_obj = User.objects.get(pk=user_id)
            user_serializer = UserSerializer(user_obj).data
            return Response({
                'status': 200,
                'message': '查询单个用户成功',
                'result': user_serializer
            })
        else:
            user_obj = User.objects.all()
            user_serializer = UserSerializer(user_obj, many=True).data
            return Response({
                'status': 200,
                'message': '查询所有用户成功',
                'result': user_serializer
            })

    def post(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, dict) or data == {}:
            return Response({
                'status': 400,
                'messages': '参数错误',
            })
        user_deserializer = UserDeSerializer(data=data)
        if user_deserializer.is_valid():
            user_save = user_deserializer.save()
            return Response({
                'status': 200,
                'message': '新增用户成功',
                'result': UserSerializer(user_save).data,
            })
        else:
            return Response({
                'status': 400,
                'message': '新增用户失败',
                'result': user_deserializer.errors
            })