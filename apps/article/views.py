from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from apps.article.forms import Article_form
from website import settings
import os
import random
from .models import Article_add
# Create your views here.
@login_required(login_url='/login')
def article_Add(request):
    if request.method == 'GET':
        return render(request,'pc/articlesadd.html')
    if request.method == 'POST':
        forms = Article_form(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            content =  request.POST.get('content')
            desc = request.POST.get('desc','')
            keywords = request.POST.get('keywords','')
            list_pic = request.POST.get('list_pic','')
            authors = request.POST.get('authors','')
            add_time = request.POST.get('add_time','')
            article = Article_add()
            article.title=title
            article.content=content
            article.desc=desc
            article.keywords=keywords
            article.list_pic=list_pic
            article.authors_id=authors
            article.add_time=add_time

            article.save()
           # Article_add.objects.create(title=title,content=content,desc=desc,keywords=keywords,list_pic=list_pic,authors_id=authors)
            return redirect('/index')


        return render(request,'pc/articlesadd.html')

def Article_list(request):
    article=Article_add.objects.all()
    return render(request,'pc/index.html',{'article':article})



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

