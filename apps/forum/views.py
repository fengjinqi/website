from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.forum.forms import Forum_form, ParentComment
from apps.forum.models import Forum_plate, Forum, Comment, Parent_Comment
from apps.forum.serializers import Forum_plateSerializers, ForumSerializers, CommentSerializers, \
    Pernents_CommentSerializers
from apps.uitls.permissions import IsOwnerOr, IsOwnerOrReadOnly
from apps.user.models import UserMessage, User


def index(request):
    """
    帖子首页
    :param request:
    :return:
    """
    plate = Forum_plate.objects.all()
    forum = Forum.objects.all()
    job = Forum.objects.filter(category__name='求职招聘')

    return render(request,'pc/forum.html',locals())


@login_required(login_url='/login')
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


def forum_category(request,category):
    """
    分类
    :param request:
    :param category:
    :return:
    """
    cate_list = Forum.objects.filter(category_id=category)
    plate = Forum_plate.objects.all()

    job = Forum.objects.filter(category__name='求职招聘')
    type = get_object_or_404(Forum_plate,pk=category)
    Forum.objects.filter()

    return render(request,'pc/forum_category.html',locals())


def forum_detail(request,forum_id):
    """
    详情
    :param request:
    :param forum_id:
    :return:
    """
    dicts = get_object_or_404(Forum,pk=forum_id)
    dicts.click_nums+=1
    dicts.save()
    if request.method == 'POST':
        forms = ParentComment(request.POST)
        if forms.is_valid():
            try:
                data = Parent_Comment()
                data.forums = forms.cleaned_data.get('forums')
                data.user = forms.cleaned_data.get('user')
                data.comments = forms.cleaned_data.get('comments')
                data.parent_comments = forms.cleaned_data.get('parent_comments')
                data.to_Parent_Comments = forms.cleaned_data.get('to_Parent_Comments')
                data.url = forms.cleaned_data.get('url')
                data.address = request.POST.get('address')
                data.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception as e:
                return JsonResponse({"code": 400, "data": "发布失败"})
    return render(request,'pc/forum_detail.html',{'dicts':dicts})


@receiver(post_save, sender=Parent_Comment)
def my_callback_reply(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """
    try:
        message = UserMessage()
        message.user_id = kwargs['instance'].to_Parent_Comments_id
        message.ids = kwargs['instance'].forums_id
        message.to_user_id = kwargs['instance'].user.id
        message.has_read = False
        message.url =kwargs['instance'].url
        message.message = "你参与的 %s 帖子评论有人回复了,快去看看吧!"%kwargs['instance'].parent_comments.forums.title
        message.save()
    except Exception as e:
        pass






class Forum_plateView(mixins.UpdateModelMixin,mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    """TODO 版块分類"""
    queryset = Forum_plate.objects.all()
    serializer_class = Forum_plateSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


class ForumView(viewsets.ModelViewSet):
    """TODO 帖子"""
    queryset = Forum.objects.all()
    serializer_class = ForumSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


class CommentView(viewsets.ModelViewSet):
    """TODO 评论"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


@receiver(post_save, sender=Comment)
def my_callback(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """

    message = UserMessage()
    message.user=kwargs['instance'].forums.authors
    message.ids = kwargs['instance'].forums.id
    message.to_user_id = kwargs['instance'].user_id
    message.has_read = False
    message.url =kwargs['instance'].url
    message.message="你的%s帖子被人评论了,快去看看吧!"%kwargs['instance'].forums.title
    message.save()




class Parent_CommentView(viewsets.ModelViewSet):
    """TODO 评论回复"""
    queryset = Parent_Comment.objects.all()
    serializer_class = Pernents_CommentSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
