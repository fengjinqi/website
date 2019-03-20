#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django.conf.urls import url
from django.urls import path, include
app_name='course'
from . import views
urlpatterns = [

  path('',views.List,name='index'),

  path('<uuid:course_id>/<str:list_id>.html/',views.Detail,name='detail'),


  path('api/<uuid:courses_id>/',views.courseViewApi,name='courseViewApi'),

]
