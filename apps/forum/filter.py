#!/usr/bin/python  
# -*- coding:utf-8 -*-  
import django_filters

from .models import Forum


class ForumFilter(django_filters.rest_framework.FilterSet):

    category = django_filters.rest_framework.BaseInFilter(field_name='category_id')
    title = django_filters.rest_framework.CharFilter(field_name='title', lookup_expr='icontains')
    category_name = django_filters.rest_framework.CharFilter(method='category_filter',label='分类标题')

    def category_filter(self, queryset,name,value):
        return Forum.objects.filter(category__name__icontains=value)

    class Meta:
        model = Forum
        fields = ['category','title','category_name' ]