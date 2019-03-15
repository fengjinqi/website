from __future__ import absolute_import

import datetime
from time import sleep

import requests
from celery import shared_task





from django.core.mail import send_mail

from random import Random
import random

from apps.article.models import Headlines
from apps.user.models import VerifyCode
from website import settings
from website.celery import app


def random_str(randomlength=8):
    str=""
    chars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lenght = len(chars)-1
    for i in range(randomlength):
        str+=chars[random.randint(0,lenght)]
    print(str)
    return str


@app.task()
def send_register_email(email,username=None,token=None,send_type='register'):
    """
    登录注册等邮件发送
    :param email:
    :param username:
    :param token:
    :param send_type:
    :return:
    """
    code = random_str(4)
    email_title = ''
    email_body = ''
    if send_type =='register':
        email_title = '注册用户验证信息'
        email_body = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证,该链接1个小时内有效',
                                 '/'.join([settings.DOMAIN, 'activate', token])])
        print('========发送邮件中')
        send_stutas = send_mail(email_title,email_body,settings.EMAIL_HOST_USER,[email])

        if send_stutas:
            print('========发送成功')
            pass
    elif send_type == 'forget':
        VerifyCode.objects.create(code=code, email=email, send_type=send_type)
        email_title = '密码重置链接'
        email_body = "你的密码重置验证码为:{0}。如非本人操作请忽略,此验证码30分钟后失效。".format(code)
        print('========发送邮件中')
        send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
        if send_stutas:
            print('========发送成功')
            pass
    elif send_type =='update_email':
        VerifyCode.objects.create(code=code, email=email, send_type=send_type)
        email_title = '修改邮箱链接'
        email_body = "你的修改邮箱验证码为:{0}。如非本人操作请忽略,此验证码30分钟后失效。".format(code)
        print('========发送邮件中')
        send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
        if send_stutas:
            print('========发送成功')
            pass




@app.task()
def error_email(email,title=None,body=None):
    email_title = title
    email_body = body
    send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])









@app.task()
def add():
    print('发送邮件到**************************************************************' )
    sleep(5)  # 休息5秒
    print('success')
    return True


@app.task()
def getApi():
    print('正在获取数据...')
    url = 'http://api01.idataapi.cn:8000/article/idataapi?KwPosition=3&catLabel1=科技&apikey=Xtv7doa2SrBskcf0X7fLwfKaLEyvXycJ2RRKGPvhLisMIASRtFtmGzzIvef2QSFs'
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == requests.codes.ok:
            dict_json = r.json()
            list_dict = []
            for item in dict_json['data']:
                obj = Headlines(
                    url=item['url'],
                    title=item['title'],
                    category=item['catLabel1'],
                    conent=item['content'],
                    author_name=item['sourceType'],
                )
                list_dict.append(obj)
            Headlines.objects.bulk_create(list_dict)
            print('数据添加成功')
    except Exception:
        print('数据添加失败===正在发生邮件通知管理员')
        error_email.delay('fengjinqi@fengjinqi.com','抓取数据错误','抓取数据错误，请尽快查看')
        print('邮件发送成功')


@app.task()
def removeApi():
    # 当前日期格式
    cur_date = datetime.datetime.now().date()
    # 前一天日期
    yester_day = cur_date - datetime.timedelta(days=1)
    # 前一周日期
    day = cur_date - datetime.timedelta(days=7)
    print("=======正在删除7天前数据======")
    # 查询前一周数据,也可以用range,我用的是glt,lte大于等于
    Headlines.objects.filter(add_time__lte=day).delete()
    print('======已删除=========')
