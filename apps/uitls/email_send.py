#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.core.mail import send_mail

from random import Random
import random

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

def send_register_email(email,username=None,token=None,send_type='register'):
    code = random_str(4)

    email_title = ''
    email_body = ''
    if send_type =='register':
        email_title = '注册用户验证信息'
        email_body = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证,该链接1个小时内有效',
                                 '/'.join([settings.DOMAIN, 'activate', token])])
        send_stutas = send_mail(email_title,email_body,settings.EMAIL_HOST_USER,[email])

        if send_stutas:
            pass
    elif send_type == 'forget':
        VerifyCode.objects.create(code=code, email=email, send_type=send_type)
        email_title = '密码重置链接'
        email_body = "你的密码重置验证码为:{0}。如非本人操作请忽略,此验证码30分钟后失效。".format(code)
        send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
        if send_stutas:
            pass
    elif send_type =='update_email':
        VerifyCode.objects.create(code=code, email=email, send_type=send_type)
        email_title = '修改邮箱链接'
        email_body = "你的修改邮箱验证码为:{0}。如非本人操作请忽略,此验证码30分钟后失效。".format(code)
        send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
        if send_stutas:
            pass