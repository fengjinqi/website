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
  path('add/',views.add_forum,name='add'),
  path('detail/<uuid:forum_id>/',views.forum_detail,name='detail'),
  path('cagetory/<int:category>/',views.forum_category,name='id'),
  ]

