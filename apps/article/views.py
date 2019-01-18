from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.article.filter import GoodsFilter
from apps.article.forms import Article_form
from apps.article.serializers import ArticleSerializer, Article_CommentSerializer, ArticleCommentReply, \
    Article_CommentSerializerAdd, ArticleCommentReplySerializer, Category_ArticleSerializer
from apps.user.models import User, Follow
from website import settings
import os
import random
from .models import Article_add, Category_Article, Article_Comment
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

def Article(request):
    """
    文章list
    :param request:
    :return:
    """
    article = Article_add.objects.all().order_by('-add_time')
    category = Category_Article.objects.all()
    type = request.GET.get('type', '')
    try:
        page = request.GET.get('page', 1)
        if type:
            article =Article_add.objects.filter(category_id=type)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
    # Provide Paginator with the request object for complete querystring generation
    p = Paginator(article,2,request=request)
    people = p.page(page)
    return render(request, 'pc/article.html', {'article': people,'category':category})


# Create your views here.
@login_required(login_url='/login')
def Article_Add(request):
    """
    新增文章
    :param request:
    :return:
    """
    if request.method == 'GET':
        category = Category_Article.objects.all()
        return render(request,'pc/articlesadd.html',{"category":category})

    if request.method == 'POST':
        forms = Article_form(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            content = forms.cleaned_data.get('content')
            category = request.POST.get('category','')
            desc = request.POST.get('desc','')
            keywords = request.POST.get('keywords','')
            list_pic = request.FILES.get('list_pic','')
            authors = forms.cleaned_data.get('authors','')
            article = Article_add()
            article.title=title
            article.content=content
            article.desc=desc
            article.keywords=keywords
            article.authors = authors
            article.category_id = int(category)
            article.list_pic = list_pic
            try:
                article.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception:
                return JsonResponse({"code":400,"data":"发布失败"})
        return JsonResponse({"code": 400, "data": "验证失败"})


@login_required(login_url='/login')
def ArticleUpdate(request,article_id):
    """
    文章修改
    :param request:
    :param article_id:
    :return:
    """
    if request.method == 'GET':
        category = Category_Article.objects.all()
        try:
            article = Article_add.objects.get(id=article_id)
        except Exception:
            return Http404
        print(article)
        return render(request, 'pc/article_update.html', {'article': article, 'category': category})
    if request.method == 'POST':
        forms = Article_form(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            content = forms.cleaned_data.get('content')
            category = request.POST.get('category', '')
            desc = request.POST.get('desc', '')
            keywords = request.POST.get('keywords', '')
            type = request.POST.get('type','')
            if type:
                list_pic = request.FILES.get('list_pic', '')
            else:
                list_pic = request.POST.get('list_pic', '')
            authors = forms.cleaned_data.get('authors', '')
            article = Article_add.objects.get(id=article_id)
            article.title = title
            article.content = content
            article.desc = desc
            article.keywords = keywords
            article.authors = authors
            article.category_id = int(category)
            article.list_pic = list_pic
            try:
                article.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception:
                return JsonResponse({"code": 400, "data": "发布失败"})
        return JsonResponse({"code": 400, "data": "验证失败"})


@login_required(login_url='/login')
@require_POST
def RemoveImage(request,article_id):
    """
    删除图片
    :param request:
    :param article_id:
    :return:
    """
    if request.method == 'POST':
        article = Article_add.objects.get(id=article_id)
        article.list_pic=''
        article.save()
        return JsonResponse({'data':200})

def Article_list(request):
    """
    首页
    :param request:
    :return:
    """
    article=Article_add.objects.filter(is_show=True).order_by('-add_time')
    popular = Article_add.objects.filter(is_show=True).order_by('click_nums')[:5]
    #user = Follow.objects.values('follow_id').distinct().order_by('-follow_id')
    user = Follow.objects.values('follow_id').distinct().order_by('-follow_id')
    item=[]
    for i in user:
        data={}
        #print(User.objects.filter(follow__follow__id=i['follow_id']))
        data['data']=User.objects.filter(follow__follow__id=i['follow_id']).distinct()
        print(data)
        item.append(data)
    #print(item)
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
    # Provide Paginator with the request object for complete querystring generation
    p = Paginator(article,2,request=request)
    people = p.page(page)
    return render(request, 'pc/index.html', {'article':people,'popular':popular,'count':item})




def Article_detail(request,article_id):
    """
    文章详情页
    :param request:
    :param article_id:
    :return:
    """
    try:
        article=Article_add.objects.get(id=article_id)
        article.click_nums+=1
        article.save()
    except Exception:
        return Http404
    return render(request,'pc/article_detail.html',{'article':article,'id':article_id})


# 写博客上传图片
@login_required(login_url='/login')
@csrf_exempt
def blog_img_upload(request):
    if request.method == "POST":
        data = request.FILES['editormd-image-file']
        img = Image.open(data)
        width = img.width
        height = img.height
        rate = 1.0  # 压缩率

        # 根据图像大小设置压缩率
        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)  # 新的宽
        height = int(height * rate)  # 新的高

        img.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图

        url = 'blogimg/' + data.name
        print(request.build_absolute_uri(settings.MEDIA_URL+data.name))
        name = settings.MEDIA_ROOT + '/' + url
        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogimg/' + data.name
            name = settings.MEDIA_ROOT + '/' + url
        try:
            img.save(name)
            print(name)
            #url = '/static'+name.split('static')[-1]
            url = request.build_absolute_uri(settings.MEDIA_URL+'blogimg/'+data.name)
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})



"""==========================================api"""

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    # page_size_query_param = 'page_size'#每页设置展示多少条
    # page_query_param = 'page'
    # max_page_size = 100


class ArticleListView(viewsets.ReadOnlyModelViewSet):
    """
     TODO 列出所有的文章 详情页
    """
    queryset = Article_add.objects.filter(is_show=True).order_by('-add_time')
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination


class FollowListView(viewsets.ReadOnlyModelViewSet):
    """
    TODO 我关注的文章
    """
    queryset = Article_add.objects.filter(is_show=True).order_by('-add_time')
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):

        queryset = Article_add.objects.filter(authors__follow__fan_id=self.request.user.id).filter(is_show=True).order_by('-add_time')
        serializer = ArticleSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class ArticleCommintView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """TODO 評論"""
    serializer_class = Article_CommentSerializerAdd
    queryset = Article_Comment.objects.all()


class ArticleCommentReplyView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """TODO 回復評論"""
    serializer_class = ArticleCommentReplySerializer
    queryset = ArticleCommentReply.objects.all()


class CategoryView(viewsets.ReadOnlyModelViewSet):
    """TODO 分類"""
    queryset = Category_Article.objects.all()
    serializer_class = Category_ArticleSerializer