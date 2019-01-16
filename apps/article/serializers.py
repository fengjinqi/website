#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from .models import Article_add, Category_Article,Article_Comment,ArticleCommentReply
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','user_imag','id')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class Category_ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Article
        fields = ('name','id',)


class Article_CommentSerializerAdd(serializers.ModelSerializer):

    class Meta:
        model = Article_Comment
        fields = '__all__'


class ArticleCommentReplySerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = ArticleCommentReply
        fields = '__all__'


class ArticleCommentReplySerializer1(serializers.ModelSerializer):
    """回复"""
    user = UserSerializer()
    to_uids = UserSerializer()
    class Meta:
        model = ArticleCommentReply
        fields = '__all__'


class Article_CommentSerializer(serializers.ModelSerializer):
    #评论
    # def to_representation(self, instance):
    #     res=super().to_representation(instance=instance)
    #     if res['aomments_id'] is None:
    #         print(res)
    #         return res
    #     else:
    #         print('ok')
    #         pass
    #         return
    #sub_cat = Article_CommentSerializer1(many=True)
    user = UserSerializer()
    articlecommentreply_set = ArticleCommentReplySerializer1(many=True,read_only=True)

    class Meta:
        model = Article_Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    #文章
    authors = UserSerializer()
    category = Category_ArticleSerializer()
    article_comment_set = Article_CommentSerializer(many=True)
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Article_add
        fields = '__all__'


