#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django.conf.urls import url
from django.urls import path, include
app_name='course'
from . import views
urlpatterns = [

  path('',views.List,name='index'),
  path('<uuid:course_id>/',views.Detail,name='detail'),

]
