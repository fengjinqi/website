#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers
from .models import Banners,Emails,link


class BannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields ='__all__'


class EmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields ='__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = link
        fields ='__all__'
