#!/usr/bin/python  
# -*- coding:utf-8 -*-
from django.urls import path
app_name='dynamic'
from . import views
urlpatterns = [
  path('',views.Home,name='index'),

]
