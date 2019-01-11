#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from apps.article.models import User
from apps.article.serializers import ArticleSerializer


class UserSerializer(serializers.ModelSerializer):
    article_add_set = ArticleSerializer(many=True)

    class Meta:
        model = User
        fields = ('id','username','mobile','user_imag','email','article_add_set',)