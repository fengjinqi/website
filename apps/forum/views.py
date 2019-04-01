from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.forum.forms import Forum_form
from apps.forum.models import Forum_plate, Forum
from apps.forum.serializers import Forum_plateSerializers, ForumSerializers
from apps.uitls.permissions import  IsOwnerOr


def index(request):
    """
    帖子首页
    :param request:
    :return:
    """
    plate = Forum_plate.objects.all()
    forum = Forum.objects.all()
    return render(request,'pc/forum.html',locals())


def add_forum(request):
    """
    新增帖子
    :param request:
    :return:
    """
    category = Forum_plate.objects.all()
    if request.method == 'POST':
        form = Forum_form(request.POST)
        if form.is_valid():
            forum = Forum()
            forum.title = form.cleaned_data.get('title')
            forum.category_id = form.cleaned_data.get('category')
            forum.keywords = form.cleaned_data.get('keywords')
            forum.content = form.cleaned_data.get('content')
            forum.authors = form.cleaned_data.get('authors')
            try:
                forum.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception:
                return JsonResponse({"code": 400, "data": "发布失败"})
    return render(request,'pc/forum_add.html',locals())



def forum_detail(request,forum_id):
    dicts = get_object_or_404(Forum,pk=forum_id)
    dicts.click_nums+=1
    dicts.save()
    return render(request,'pc/forum_detail.html',locals())




class Forum_plateView(mixins.UpdateModelMixin,mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    """TODO 版块分類"""
    queryset = Forum_plate.objects.all()
    serializer_class = Forum_plateSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


class ForumView(viewsets.ModelViewSet):
    """TODO 版块分類"""
    queryset = Forum.objects.all()
    serializer_class = ForumSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]