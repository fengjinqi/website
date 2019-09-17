import datetime
import json
from django.db.models import Q, Count
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse,Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import requests
import urllib3
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.filter import  ArticleFilter
from apps.article.forms import Article_form
from apps.article.serializers import ArticleSerializer, Article_CommentSerializer, ArticleCommentReply, \
    Article_CommentSerializerAdd, ArticleCommentReplySerializer, Category_ArticleSerializer, ArticleCreatedSerializer, \
    ArticleCommitSerializer
from apps.forum.models import Forum
from apps.support.models import link, QQ, Banners, Seo
from apps.uitls.jsonserializable import DateEncoder
from apps.uitls.permissions import IsOwnerOrReadOnly, IsOwnerOr
from apps.user.models import User, Follows, UserMessage
from website import settings
import os
import random
from .models import Article, Category_Article, Article_Comment, Recommend, Headlines
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

def test(request):
    WorkList = []
    for i in range(1,100):
        WorkList.append(Forum(title='```cpp\n下例 中的某些语句读不太明白：\n 1.   DataTable dt=ds.Tables[\"cs\"] 这句最难理解，意思是读取cs表赋给新建的内存表dt（复制表）?还是dt表指向（引用）cs表，修改dt其实就是修改cs?\n 2.   sda.FillSchema(dt,SchemaType.Mapped); 这句应该是将数据库表中的元数据填入到dt中，为何要填入?cs表中没有元数据吗?\n 3.   此例中修改了dt表，执行Update为何更新了数据库?dt、cs与数据库是个怎么个联系?\n\n\n例：\nSqlConnection ds;\nDataSet ds;\nSqlDataAdapter sda;\n...........        \nDataTable dt=ds.Tables[\"cs\"];\nsda.FillSchema(dt,SchemaType.Mapped);\nDataRow dr=dt.Rows.Find(txtNo.text);\ndr[\"姓名\"]=txtName.Text.Trim();\ndr[\"性别\"]=txtSex.Text.Trim();\nSqlCommandBuilder cmdbuilder=new SqlCommandBuilder(sda);\nsda.Update(dt);\n```%s'%(i),category_id=4,authors_id='2a5ec3edf61c43a6a547851e9ba15071'))
    Forum.objects.bulk_create(WorkList)
    return HttpResponse('ok')


def Home(request):
    """
    首页
    :param request:
    :return:
    """
    recommend = Recommend.objects.filter(is_recommend=True)[:10]
    seo_list = get_object_or_404(Seo, name='首页')
    qq = QQ.objects.all()
    links = link.objects.all()
    #user = Follow.objects.values('follow_id').distinct().order_by('-follow_id')
    # user = Follows.objects.values('follow_id').distinct().order_by('-follow_id')
    # item=[]
    # for i in user:
    #     data={}
    #     #print(User.objects.filter(follow__follow__id=i['follow_id']))
    #     data['data']=User.objects.filter(follow__follow__id=i['follow_id']).distinct()
    #     item.append(data)
    try:
        page = request.GET.get('page',1)
        if page == '':
                page = 1
    except PageNotAnInteger:
        page = request.GET.get('page')
    # Provide Paginator with the request object for complete querystring generation
    article = Article.objects.filter(is_show=True)[:100]
    p = Paginator(article,10,request=request)
    people = p.page(page)
    banners = Banners.objects.first()
    return render(request, 'pc/index.html', {'seo_list':seo_list,'article':people,'qq':qq,'recommend':recommend,'links':links,'banners':banners})


def ArticleList(request):
    """
    文章list
    :param request:
    :return:
    """
    seo_list = get_object_or_404(Seo, name='文章')
    article = Article.objects.filter(is_show=True)
    category = Category_Article.objects.all().order_by('order')
    type = request.GET.get('type', '')
    try:
        page = request.GET.get('page', 1)
        if type:
            article =Article.objects.filter(category_id=type,is_show=True)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
    # Provide Paginator with the request object for complete querystring generation
    p = Paginator(article,10,request=request)
    people = p.page(page)

    headlines = Headlines.objects.all()[:30]
    banners = Banners.objects.first()
    return render(request, 'pc/article.html', {'seo_list':seo_list,'article': people,'category':category,'Headlines':headlines,'banners':banners})


def api(request):

    url =  'http://v.juhe.cn/toutiao/index?type=keji&key={0}'.format(conf.get('AppKey','key'))
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }

    # r = requests.get(url, headers=headers)
    # print(r.json())
    # if r.status_code == requests.codes.ok:
    #
    #     dict_json = r.json()
    #     print(dict_json['result']['data'])
    #     main = Headlines()
    #     list_dict = []
    #     for item in dict_json['result']['data']:
    #         obj = Headlines(
    #         url = item['url'],
    #         title = item['title'],
    #         category = item['category'],
    #         #conent = item['content'],
    #         author_name = item['author_name'],
    #         )
    #         list_dict.append(obj)
    #     Headlines.objects.bulk_create(list_dict)
    #     error_email.delay('fengjinqi@fengjinqi.com', '抓取数据错误', '抓取数据错误，请尽快查看')
    # http = urllib3.PoolManager()
    # fields = {
    #     'KwPosition':'3',
    #     'catLabel1':'科技',
    #     'apikey':'Xtv7doa2SrBskcf0X7fLwfKaLEyvXycJ2RRKGPvhLisMIASRtFtmGzzIvef2QSFs'
    # }
    # r = http.request('GET',url='http://api01.idataapi.cn:8000/article/idataapi',fields=fields,headers=headers)
    # print(r.data.decode('utf-8'))
    # r = requests.get('http://v.juhe.cn/toutiao/index?type=keji&key=06207ed4627997cd7ec09c6d5eb95a61')
    # print(r.status_code)
    # for i in r.json():
    #     print(i)
    cur_date = datetime.datetime.now().date()

    # 前四天
    day = cur_date - datetime.timedelta(days=7)

    # 查询前一周数据,也可以用range,我用的是glt,lte大于等于
    Headlines.objects.filter(add_time__lte=day).delete()


    return HttpResponse({'ee':'43'})


from apps.article.tasks import add, error_email, conf


def addModel(request):
    add.delay()
    print('定时任务')

    return HttpResponse('ok')







@login_required(login_url='/login')
def ArticleMe(request):

    """
    我关注的人文章
    :param request:
    :return:
    """
    article = Article.objects.filter(authors__follow__fan_id=request.user.id,is_show=True)

    category = Category_Article.objects.all()
    type = request.GET.get('type', '')
    try:
        page = request.GET.get('page', 1)
        if type:
            article =Article.objects.filter(authors__follow__fan_id=request.user.id,category_id=type,is_show=True)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
    p = Paginator(article,10,request=request)
    people = p.page(page)
    # url = 'http://api01.idataapi.cn:8000/article/idataapi?KwPosition=3&catLabel1=科技&apikey=Xtv7doa2SrBskcf0X7fLwfKaLEyvXycJ2RRKGPvhLisMIASRtFtmGzzIvef2QSFs'
    # headers = {
    #     "Accept-Encoding": "gzip",
    #     "Connection": "close"
    # }
    # r = requests.get(url, headers=headers)
    headlines = Headlines.objects.all()[:20]
    banners = Banners.objects.first()
    return render(request, 'pc/article_me.html', {'article': people,'category':category,'Headlines':headlines,'banners':banners})


# Create your views here.
@login_required(login_url='/login')
def Article_Add(request):
    """
    新增文章
    :param request:
    :return:
    """
    seo_list = get_object_or_404(Seo, name='文章')
    if request.method == 'GET':
        category = Category_Article.objects.all()
        return render(request,'pc/articlesadd.html',{"category":category,'seo_list':seo_list})

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
            article = Article()
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
            article = Article.objects.get(id=article_id)
        except Exception:
            return Http404
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
            article = Article.objects.get(id=article_id)
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


#@login_required(login_url='/login')
@require_POST
@csrf_exempt
def ArticleDelete(request):
    """
    删除文章
    :param request:
    :return:
    """
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        user = json.loads(request.body)['username']
        if id and user:
            Article.objects.filter(id=id, authors_id=user).update(is_show=False)
            return JsonResponse({'status':200,'message':'删除成功'})
        return JsonResponse({'status':400,'message':'删除失败'})


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
        article = Article.objects.get(id=article_id)
        article.list_pic=''
        article.save()
        return JsonResponse({'data':200})


def Article_detail(request,article_id):
    """
    文章详情页
    :param request:
    :param article_id:
    :return:
    """
    try:
        article=Article.objects.get(id=article_id)
        id = article.category.id
        article.click_nums+=1
        article.save()
    except Exception:
        return Http404

    content = Article.objects.filter(category_id=id).exclude(id=article_id).order_by('-click_nums')[:10]
    #print(content.annotate())
    return render(request,'pc/article_detail.html',{'article':article,'id':article_id,'content':content})


# 写博客上传图片
# @login_required(login_url='/login')
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
    page_size = 10
    # page_size_query_param = 'page_size'#每页设置展示多少条
    # page_query_param = 'page'
    # max_page_size = 100


class ArticleListView(viewsets.ReadOnlyModelViewSet):
    """
     TODO 列出所有的文章 详情页
    """
    queryset = Article.objects.filter(is_show=True).order_by('-add_time')
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticleFilter
    #permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    #authentication_classes = [JSONWebTokenAuthentication]

class MeArticleListView(viewsets.ReadOnlyModelViewSet):
    """
     TODO 我的的文章 详情页
    """
    queryset = Article.objects.filter(is_show=True).order_by('-add_time')
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticleFilter
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        return Article.objects.filter(authors_id=self.request.user.id).filter(is_show=True).order_by(
            '-add_time')



class FollowListView(viewsets.ReadOnlyModelViewSet):
    """
    TODO 我关注的文章
    """
    queryset = Article.objects.filter(is_show=True).order_by('-add_time')
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]
    def list(self, request, *args, **kwargs):

        queryset = Article.objects.filter(authors__follow__fan_id=self.request.user.id).filter(is_show=True).order_by('-add_time')
        serializer = ArticleSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class ArticleCreated(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    """
    创建文章
    """
    queryset = Article.objects.filter(is_show=True)
    serializer_class = ArticleCreatedSerializer
    permission_classes = (IsAuthenticated,IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]


class ArticleCommintView(mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):

    """TODO 評論"""
    #serializer_class = Article_CommentSerializerAdd
    queryset = Article_Comment.objects.all()
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action =='retrieve':
            return []
        else:
            return [IsAuthenticated(),IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list':
            return Article_CommentSerializer
        elif self.action == 'retrieve':
            return Article_CommentSerializer
        else:
            return Article_CommentSerializerAdd


@receiver(post_save, sender=Article_Comment)
def my_callback(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """

    message = UserMessage()
    message.user=kwargs['instance'].article.authors
    message.ids = kwargs['instance'].article.id
    message.to_user_id = kwargs['instance'].user_id
    message.has_read = False
    message.url =kwargs['instance'].url
    message.message="你的%s文章被人评论了,快去看看吧!"%kwargs['instance'].article.title
    message.save()


class ArticleCommentReplyView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """TODO 回復評論"""
    serializer_class = ArticleCommentReplySerializer
    queryset = ArticleCommentReply.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]

@receiver(post_save, sender=ArticleCommentReply)
def my_callback_reply(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """
    message = UserMessage()
    message.user = kwargs['instance'].to_uids
    message.ids = kwargs['instance'].aomments_id.article.id
    message.to_user = kwargs['instance'].user
    message.has_read = False
    message.url =kwargs['instance'].url
    message.message = "你参与的 %s 文章评论有人回复了,快去看看吧!"%kwargs['instance'].aomments_id.article.title
    message.save()


class CategoryView(mixins.UpdateModelMixin,mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    """TODO 分類"""
    queryset = Category_Article.objects.all()
    serializer_class = Category_ArticleSerializer
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated(),IsOwnerOrReadOnly()]


class ArticleCommit(viewsets.ModelViewSet):
    """文章推荐"""
    queryset = Recommend.objects.filter(is_recommend=True)
    serializer_class = ArticleCommitSerializer
    permission_classes = (IsAuthenticated,)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]