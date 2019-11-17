#!/usr/bin/python  
# -*- coding:utf-8 -*-  
import django_filters

from .models import Article


class ArticleFilter(django_filters.rest_framework.FilterSet):

    category = django_filters.rest_framework.BaseInFilter(field_name='category_id')
    category_name = django_filters.rest_framework.CharFilter(method='category_filter',label='标题')
    title = django_filters.rest_framework.CharFilter(field_name='title', lookup_expr='icontains')

    def category_filter(self, queryset,name,value):
        return queryset.filter(category__name__icontains=value)

    class Meta:
        model = Article
        fields = ['category','title','category_name' ]