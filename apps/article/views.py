from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from apps.article.forms import Article_form
from website import settings
import os
import random
from .models import Article_add,Category_Article

def Article(request):
    article = Article_add.objects.all().order_by('-add_time')
    return render(request, 'pc/article.html', {'article': article})
# Create your views here.
@login_required(login_url='/login')
def Article_Add(request):
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

def Article_list(request):
    article=Article_add.objects.all().order_by('-add_time')
    popular = Article_add.objects.all().order_by('click_nums')[:5]
    user = Article_add.objects.filter(authors_id=request.user.id).count()
    print(user)
    return render(request, 'pc/index.html', {'article':article,'popular':popular,'count':user})




def Article_detail(request,article_id):
    print(article_id)
    try:
        article=Article_add.objects.get(id=article_id)
        article.click_nums+=1
        article.save()
    except Exception:
        return Http404
    return render(request,'pc/article_detail.html',{'article':article})

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

