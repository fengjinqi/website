#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from .models import Article_add, Category_Article,Article_Comment
from apps.user.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','user_imag',)


class Category_ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Article
        fields = ('name',)


class Article_CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Article_Comment
        fields = '__all__'


class Article_CommentSerializer1(serializers.ModelSerializer):
    sub_cat = Article_CommentSerializer(many=True)
    class Meta:
        model = Article_Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    authors = UserSerializer()
    category = Category_ArticleSerializer()
    article_comment_set = Article_CommentSerializer1(many=True)
    class Meta:
        model = Article_add
        fields = '__all__'

