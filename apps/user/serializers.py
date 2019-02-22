#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from apps.article.models import User
from apps.article.serializers import ArticleSerializer
from apps.user.models import UserMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','mobile','user_imag','email','is_active','is_staff','is_superuser')


class UserMessageSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = UserMessage
        fields = '__all__'