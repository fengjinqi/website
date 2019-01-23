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
  path('modify/', views.Modify.as_view(), name='modify'),
  path('sing_email/', views.ResetUserView.as_view(), name='sing_email'),
  path('email_update/', views.EmailView.as_view(), name='email_update'),
  path('Guan/', views.Guan, name='Guan'),
]
