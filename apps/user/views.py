import json

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import Http404, HttpResponse,JsonResponse
from django.shortcuts import render

# Create your views here.
from .forms import CaptchaTestForm
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