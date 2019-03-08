#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from apps.article.models import User
from apps.article.serializers import ArticleSerializer
from apps.user.models import UserMessage


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        res = super().to_representation(instance=instance)
        access = []
        if res['is_staff'] == True:
            access.append('is_staff')
        if res['is_superuser'] == True:
            access.append('is_superuser')
        res.setdefault('access', access)
        return res

    class Meta:
        model = User
        fields = ('id','username','mobile','user_imag','email','is_active','is_staff','is_superuser','info','position')


class UserMessageSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = UserMessage
        fields = '__all__'