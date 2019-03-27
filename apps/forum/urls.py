#!/usr/bin/python  
# -*- coding:utf-8 -*-  
#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.urls import path, include
app_name='forum'
from . import views

urlpatterns = [
  #path('',views.login_view,name='index'),
  path('',views.index,name='forum'),
  ]

