from rest_framework import serializers, exceptions
from django.conf import settings

from demo01.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()
    # 自定义
    myType = serializers.SerializerMethodField()

    # ------------------------------------------------
    gender = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()

    def get_myType(self, obj):
        return "my type"

    def get_gender(self, obj):
        # if obj.gender == 0:
        #     return '男'
        # elif obj.gender == 1:
        #     return '女'
        # else:
        #     return '保密'
        return obj.get_gender_display()

    def get_pic(self, obj):
        return f'http://127.0.0.1:8000/{settings.MEDIA_URL}{str(obj.pic)}'


class UserDeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=1)
    password = serializers.CharField()
    re_pwd = serializers.CharField()

    # 全局钩子校验
    def validate(self, attrs):
        # 验证两次密码是否一致
        password = attrs.get('password')
        re_pwd = attrs.pop('re_pwd')
        if password != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    # 局部钩子校验
    def validate_username(self, data):
        user = User.objects.filter(username=data)
        if user:
            raise exceptions.ValidationError('用户名已存在')
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)
