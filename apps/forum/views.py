import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.paginator import PageNotAnInteger
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from pure_pagination import Paginator
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.views import StandardResultsSetPagination
from apps.forum.filter import ForumFilter
from apps.forum.forms import Forum_form, ParentComment
from apps.forum.models import Forum_plate, Forum, Comment, Parent_Comment
from apps.forum.serializers import Forum_plateSerializers, ForumSerializers, CommentSerializers, \
    Pernents_CommentSerializers, CommentSerializersAdd
from apps.support.models import Seo
from apps.uitls.permissions import IsOwnerOr, IsOwnerOrReadOnly
from apps.user.models import UserMessage, User


# def get_online_count():
#     online_ips = cache.get("online_ips", [])
#     print(online_ips)
#     if online_ips:
#         #online_ips = cache.get_many(online_ips).keys()
#         return len(online_ips)
#     return 0


def index(request):
    """
    帖子首页
    :param request:
    :return:
    """
    seo_list = get_object_or_404(Seo, name='社区论坛')
    plate = Forum_plate.objects.all()
    forum = Forum.objects.filter(hidden=False)
    job = Forum.objects.filter(hidden=False,category__name='求职招聘')
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
        # Provide Paginator with the request object for complete querystring generation
    p = Paginator(forum, 10, request=request)
    people = p.page(page)
    return render(request,'pc/forum.html',locals())


@login_required(login_url='/login')
def indexMe(request):
    """
    wd帖子首页
    :param request:
    :return:
    """
    plate = Forum_plate.objects.all()
    forum = Forum.objects.filter(hidden=False)
    count = User.objects.filter(follow__fan__id=request.user.id)
    floow = User.objects.filter(fan__follow_id=request.user.id)
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
        # Provide Paginator with the request object for complete querystring generation
    p = Paginator(forum, 10, request=request)
    people = p.page(page)
    return render(request,'pc/forum_me.html',locals())


@login_required(login_url='/login')
def add_forum(request):
    """
    新增帖子
    :param request:
    :return:
    """
    category = Forum_plate.objects.all()
    seo_list = get_object_or_404(Seo, name='社区论坛')
    if request.method == 'POST':
        form = Forum_form(request.POST)
        if form.is_valid():
            forum = Forum()
            forum.title = form.cleaned_data.get('title')
            forum.category_id = form.cleaned_data.get('category')
            forum.keywords = request.POST.get('keywords')
            forum.content = form.cleaned_data.get('content')
            forum.authors = form.cleaned_data.get('authors')
            try:
                forum.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception as e:
                return JsonResponse({"code": 400, "data": "发布失败"})
        pattern = re.compile(r'<[^>]+>', re.S)
        result = pattern.sub("", str(form.errors))
        return JsonResponse({"code": 400, "data": result})
    return render(request,'pc/forum_add.html',locals())


@login_required(login_url='/login')
def update_forum(request,forum_id):
    if request.method == 'GET':
        item = get_object_or_404(Forum,pk=forum_id)
        plate = Forum_plate.objects.all()
        seos = get_object_or_404(Seo, name='社区论坛')
        return render(request,'pc/forum_update.html',{'plate':plate,'seos':seos,'forum':item})
    elif request.method == 'POST':
        form = Forum_form(request.POST)
        if form.is_valid():
            forum = get_object_or_404(Forum,pk=forum_id)
            forum.title = form.cleaned_data.get('title')
            forum.category_id = form.cleaned_data.get('category')
            forum.keywords = request.POST.get('keywords')
            forum.content = form.cleaned_data.get('content')
            forum.authors = form.cleaned_data.get('authors')
            try:
                forum.save()
                return JsonResponse({"code": 200, "data": "修改成功"})
            except Exception:
                return JsonResponse({"code": 400, "data": "修改失败"})
        else:
            pattern = re.compile(r'<[^>]+>', re.S)
            result = pattern.sub("", str(form.errors))
            return JsonResponse({"code": 400, "data": result})


@login_required(login_url='/login')
def delForum(request,id):
    """
    删除帖子
    :param request:
    :param id:
    :return:
    """
    if request.is_ajax():
        try:
            data = get_object_or_404(Forum,pk=id)
            data.hidden=True
            data.save()
            return JsonResponse({'status':200,'message':'删除成功'})
        except Exception as e:
            return JsonResponse({'status': 400, 'message': '删除失败'})


def forum_category(request,category):
    """
    分类
    :param request:
    :param category:
    :return:
    """
    cate_list = Forum.objects.filter(category_id=category,hidden=False)
    plate = Forum_plate.objects.all()

    job = Forum.objects.filter(hidden=False,category__name='求职招聘')
    type = get_object_or_404(Forum_plate,pk=category)
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
        # Provide Paginator with the request object for complete querystring generation
    p = Paginator(cate_list, 20, request=request)
    people = p.page(page)

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
    authentication_classes = [JSONWebTokenAuthentication]


class ForumView(viewsets.ModelViewSet):
    """TODO 帖子"""
    queryset = Forum.objects.filter(hidden=False)
    serializer_class = ForumSerializers
    pagination_class = StandardResultsSetPagination
    #permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    filter_backends = (DjangoFilterBackend,)
    filter_class = ForumFilter
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated(), IsOwnerOr()]

    def get_queryset(self):
        user_id = self.request.query_params.get('pk')
        if user_id:
            return Forum.objects.filter(authors_id=user_id, hidden=False)

        if self.request.user.is_superuser and self.request.user:
            return Forum.objects.filter(hidden=False)
        elif self.request.user.is_active:
            return Forum.objects.filter(authors=self.request.user,hidden=False)
        else:
            return Forum.objects.filter(hidden=False)



class CommentView(viewsets.ModelViewSet):

    """TODO 评论"""
    queryset = Comment.objects.all()
    #serializer_class = CommentSerializers
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializers
        elif self.action == 'retrieve':
            return CommentSerializers
        else:
            return CommentSerializersAdd



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
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]


@receiver(post_save, sender=Parent_Comment)
def my_callback_reply(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """
    message = UserMessage()

    message.user=kwargs['instance'].to_Parent_Comments
    message.ids = kwargs['instance'].forums.id
    message.to_user_id = kwargs['instance'].user_id
    message.has_read = False

    message.url =kwargs['instance'].url
    message.message="你参与的%s帖子评论有人回复了,快去看看吧!"%kwargs['instance'].forums.title
    message.save()