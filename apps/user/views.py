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

from apps.user.models import User, Follow
from .forms import CaptchaTestForm, LoginForms, Follow_Forms


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
    """进行邮箱登录验证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(mobile=username) | Q(email=username))
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
            print(remember)
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
                print(request.POST.get('follow'))
                print(request.user.id)
                print(request.user.id == request.POST.get('follow'))
                if request.POST.get('follow') == request.user.id:
                    print('====')
                    return JsonResponse({'status': 201, 'message': '不能自己关注自己'})
                else:
                    cun = Follow.objects.filter(follow=froms.cleaned_data.get('follow'),fan=request.user.id)
                    if cun:
                        cun.delete()
                        print(cun)
                        return JsonResponse({'status': 200, 'message': '已取消关注'})
                    # follow.follow = froms.cleaned_data.get('follow')
                    # follow.fan_id = request.user.id
                    # follow.save()
                    #print(request.user.id)
                    return JsonResponse({'status':200,'message':'成功关注'})
        return JsonResponse({"status":302,"message":"未登录"})