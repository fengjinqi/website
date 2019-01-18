#!/usr/bin/python  
# -*- coding:utf-8 -*-  
#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.urls import path, include
app_name='user'
from . import views
urlpatterns = [
  #path('',views.login_view,name='index'),
  path('',views.Person.as_view(),name='person'),
  path('author/',views.Author.as_view(),name='author'),
  path('<uuid:article_id>/',views.PersonDetaile.as_view(),name='author_detaile'),
  path('profile/', views.Profile,name='profile'),
  path('info/', views.Info, name='info'),
]
