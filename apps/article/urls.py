#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django.conf.urls import url
from django.urls import path, include
app_name='article'
from . import views
urlpatterns = [
  path('',views.article_Add,name='index'),

  path('blog_img_upload/',views.blog_img_upload,name='blog_img_upload')
]
