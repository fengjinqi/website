#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from .models import Article_add, Category_Article
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','user_imag',)


class Category_ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Article
        fields = ('name',)

class ArticleSerializer(serializers.ModelSerializer):
    authors = UserSerializer()
    category = Category_ArticleSerializer()
    class Meta:
        model = Article_add
        fields = '__all__'

