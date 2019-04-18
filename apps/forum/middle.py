from datetime import datetime

from django.contrib.sessions.models import Session
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.utils.timezone import now, timedelta

class Row1(MiddlewareMixin):
    def process_request(self,request):
        print("中间件1请求")
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        print(ip)
    def process_response(self,request,response):
        print("中间件1返回")

        # print(now().date() + timedelta(days=-1))
        # print(datetime.now().date())
        return response


class ZxMiddleware():


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

    def process_request(self, request):
        print(request.META['HTTP_X_FORWARDED_FOR'])
        # if 'HTTP_X_FORWARDED_FOR' in request.META:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # else:
        #     ip = request.META['REMOTE_ADDR']
        # online_ips = cache.get("online_ips", [])
        # if online_ips:
        #     online_ips = cache.get_many(online_ips).keys()
        # cache.set(ip, 0, 15 * 60)
        # if ip not in online_ips:
        #     online_ips.append(ip)
        # cache.set("online_ips", online_ips)