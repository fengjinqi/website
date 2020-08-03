#!/usr/bin/python  
# -*- coding:utf-8 -*-
from django.urls import path
app_name='article'
from . import views
urlpatterns = [

  path('', views.ArticleList, name='index'),

  path('created/',views.Article_Add,name='created'),
  path('me/',views.ArticleMe,name='me'),
  path('',views.ArticleList,name='index'),
  path('blog_img_upload/',views.blog_img_upload,name='blog_img_upload'),
  path('detail/<uuid:article_id>',views.Article_detail,name='detail'),
  path('update/<uuid:article_id>',views.ArticleUpdate,name='update'),
  path('update_image/<uuid:article_id>',views.RemoveImage,name='update_image'),
  path('delete/',views.ArticleDelete,name='delete'),
]
