#!/usr/bin/python  
# -*- coding:utf-8 -*-  
import django_filters

from .models import Courses


class CoursesFilter(django_filters.rest_framework.FilterSet):

    title = django_filters.rest_framework.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Courses
        fields = ['title', ]