#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from apps.article.models import User
from apps.article.serializers import ArticleSerializer
from apps.user.models import UserMessage, Follows


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
        fields = ('id','username','mobile','user_imag','user_image','email','is_active','is_staff','is_superuser','info','position')


class UserMessageSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = UserMessage
        fields = '__all__'


class FollowsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):

        access = None
        res = super(FollowsSerializer, self).to_representation(instance=instance)
        is_active = Follows.objects.filter(follow=res.get('fan')['id'], fan=res.get('follow')['id']).exists()
        access=is_active
        res.setdefault('access', access)
        return res
    fan = UserSerializer()
    follow = UserSerializer()

    class Meta:
        model = Follows
        fields = '__all__'


class FollowsSerializerAdd(serializers.ModelSerializer):

    class Meta:
        model = Follows
        fields = '__all__'


class FollowsOthesSerializer(serializers.ModelSerializer):
    """TODO 查询其它用户的粉丝与关注并且当前用户是否关注"""
    def to_representation(self, instance):
        access = None
        res = super(FollowsOthesSerializer, self).to_representation(instance=instance)
        fan = self.context['request'].query_params.get('fan')
        follow = self.context['request'].query_params.get('follow')
        if fan:
            try:

                is_active = Follows.objects.filter(fan=self.context['request'].query_params.get('user_id'),follow=res.get('fan')['id']).exists()
                access = is_active
            except Exception as e:
                access = False
            res.setdefault('access', access)
            return res
        elif follow:
            try:
                is_active = Follows.objects.filter(fan=self.context['request'].query_params.get('user_id'),
                                                   follow=res.get('follow')['id']).exists()
                access = is_active
            except Exception as e:
                access = False
            res.setdefault('access', access)
            return res

    fan = UserSerializer()
    follow = UserSerializer()

    class Meta:
        model = Follows
        fields = '__all__'