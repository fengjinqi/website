"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from apps.user.views import test,captcha_refresh,yan
from django.views.generic import TemplateView

from website import settings
from apps.article import views
from apps.user.views import logout_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register('article_list', views.ArticleListView)
router.register('follow_list', views.FollowListView)
router.register('article_Comment', views.ArticleCommintView)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('',test), # 这是生成验证码的图片
    url(r'^captcha/', include('captcha.urls')),
    path('refresh/',captcha_refresh), # 这是生成验证码的图片
    path('yan/',yan), # 这是生成验证码的图片
    path('index/',views.Article_list,name='home'),
    path('login/',include('apps.user.urls')),
    path('logou/',logout_view,name='logou'),
    path('register/',TemplateView.as_view(template_name='pc/register.html')),
    path('article/',include('apps.article.urls')),



    re_path(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATI_ROOT})  # 配置文件上传html显示
]
