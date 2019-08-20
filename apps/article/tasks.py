from __future__ import absolute_import

import datetime
from configparser import ConfigParser
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
        print(send_stutas)
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
def error_email(title=None,body=None,email=None):
    email_title = title
    email_body = body
    send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])









@app.task()
def add():
    print('发送邮件到**************************************************************' )
    sleep(5)  # 休息5秒
    print('success')
    return True


conf = ConfigParser()
conf.read('config.ini')


@app.task()
def getApi():
    print('正在获取数据...')

    #url = 'http://api01.idataapi.cn:8000/article/idataapi?KwPosition=3&catLabel1=科技&apikey={0}'.format(conf.get('iDataApi','key'))
    url = 'http://v.juhe.cn/toutiao/index?type=keji&key={0}'.format(conf.get('AppKey','key'))
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == requests.codes.ok:
            dict_json = r.json()
            list_dict = []
            for item in dict_json['result']['data']:
                # obj = Headlines(
                #     url=item['url'],
                #     title=item['title'],
                #     category=item['catLabel1'],
                #     conent=item['content'],
                #     author_name=item['sourceType'],
                # )
                obj = Headlines(
                    url=item['url'],
                    title=item['title'],
                    category=item['category'],
                    conent=item['title'],
                    author_name=item['author_name'],
                )
                list_dict.append(obj)
            Headlines.objects.bulk_create(list_dict)
            print('数据添加成功')
    except Exception as e:
        print('数据添加失败===正在发生邮件通知管理员',e)

        print(error_email.delay(settings.EMAIL_WEBITE_NAME,'抓取数据错误','{0}'.format(e),settings.ERROR_FROM))
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
import os
@app.task()
def backups():
    # 你需要导入这个模块 因为需要在shell中执行
    os.system("/usr/bin/mysqldump website > /data/website_$(date +%Y%m%d_%H%M%S).sql")


    print('数据库备份---')
    # os中的system模块用来将()中的代码在shell中执行
    # ()中的参数 "调用mysqldump  -uroot -ppassword 需要备份的数据库名 >  生成的文件名.sql"

    #           二     你也可以自定义保存路径(这个文件必须存在)
    # path = "d://新建文件夹//DB_name_table"
    # os.system("mysql -uroot -p%s DB_name table> %s.sql" % (key,path))    #这是对DB_name中的table表进行备份

    #os.system('mysqldump -uroot -pmysql website > /data/website/website_$(date +%Y%m%d_%H%M%S).sql')

