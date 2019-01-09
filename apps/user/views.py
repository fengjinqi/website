import json

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import Http404, HttpResponse,JsonResponse
from django.shortcuts import render, redirect,reverse

# Create your views here.

from django.contrib.auth.views import method_decorator,login_required
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.article.models import Article_add
from apps.article.serializers import ArticleSerializer
from apps.uitls.permissions import IsOwnerOrReadOnly
from apps.user.models import User, Follow
from .forms import CaptchaTestForm, LoginForms, Follow_Forms
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.pagination import PageNumberPagination

def test(request):
    form = CaptchaTestForm()
    return render(request,'test.html',{'form':form})

def captcha_refresh(request):
    print('=========')
    """  Return json with new captcha for ajax refresh request """
    if not request.is_ajax():
 # 只接受ajax提交
        raise Http404
    new_key = CaptchaStore.generate_key()
    to_json_response = {
        'key': new_key,
        'image_url': captcha_image_url(new_key),
    }
    print(to_json_response)
    return HttpResponse(json.dumps(to_json_response), content_type='application/json')

def yan(request):
    cs = CaptchaStore.objects.filter(response=request.POST['response'], hashkey=request.POST['hashkey'])
    if cs:
        return JsonResponse({"success":"ok"})
    else:
        return JsonResponse({'error':'shibai'})




    #===============

class CustomBackend(ModelBackend):
    """进行手机登录验证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(mobile=username) | Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def login_view(request):
    if request.method == 'GET':
        return render(request,'pc/logoin.html')
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request,username=telephone,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    return JsonResponse({"code":200,"message":"","data":{}})
                    #return restful.result()
                else:
                    return JsonResponse({"code": 401, "message": "此账号暂无权限，请联系管理员", "data": {}})
                    #return restful.unauth(message='此账号暂无权限，请联系管理员')
            else:
                return JsonResponse({"code": 400, "message": "手机号码或者密码错误", "data": {}})
                #return restful.params_error(message="手机号码或者密码错误")
        else:
            errors = form.get_errors()
            return JsonResponse({"code":400,"message":"","data":errors})
            #return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect('/index')


class Author(View):
    def get(self,request):
        return
    #@method_decorator(login_required(login_url='/login'))
    def post(self,request):
        if request.user is not None and  request.user.is_authenticated:
            froms = Follow_Forms(request.POST)
            if froms.is_valid():
                follow = Follow()
                if request.POST.get('follow') == str(request.user.id):
                    return JsonResponse({'status': 201, 'message': '不能自己关注自己'})
                else:
                    cun = Follow.objects.filter(follow=froms.cleaned_data.get('follow'),fan=request.user.id)
                    if cun:
                        cun.delete()
                        return JsonResponse({'status': 200, 'message': '已取消关注'})
                    follow.follow = froms.cleaned_data.get('follow')
                    follow.fan_id = request.user.id
                    follow.save()
                    return JsonResponse({'status':200,'message':'成功关注'})
        return JsonResponse({"status":302,"message":"未登录"})


"""个人中心"""

class Person(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self,request):
        return render(request,'pc/person/index.html')





class PersonApi(viewsets.ReadOnlyModelViewSet):

    queryset = Article_add.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)#未登录禁止访问

    authentication_classes = (SessionAuthentication,)
    # def list(self, request, *args, **kwargs):
    #     queryset =  Article_add.objects.filter(authors_id=self.request.user.id).order_by('-add_time')
    #     serializer = ArticleSerializer(queryset, many=True)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     return Response(serializer.data)
    # def get_queryset(self):
    #     return Article_add.objects.filter(authors_id=self.request.user.id)