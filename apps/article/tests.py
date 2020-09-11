#!/usr/bin/env python
#-*-coding:utf-8-*-
import datetime
import os
import smtplib
from email.header import make_header
from email.message import EmailMessage

from email.mime.application import MIMEApplication

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import EmailMultiAlternatives
from django.test import TestCase

#from apps.article.models import Article



# Create your tests here.

if __name__ == '__main__':
    n= map(lambda x: x % 2, range(3))
    print('/data/website_{}.sql'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
    print(os.path.abspath('/Users/fengjinqi/fsdownload/website_20200910_010000.sql'))
    #print(n)


    # 文件路径

    address = '/Users/fengjinqi/fsdownload/website_20200910_010000.sql'
print(os.path.exists(address))
timer = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
fileName = '/data/website_{}.sql'.format(timer)
print(fileName)
print(os.path.exists(fileName))
# 如名字所示Multipart就是分多个部分
    # msg = MIMEMultipart()
    # msg["Subject"] = "网站数据库备份"
    # msg["From"] = _user
    # msg["To"] = "1218525402@qq.com"
    #
    # # ---这是文字部分---
    # part = MIMEText("网站数据库备份")
    #
    # msg.attach(part)
    #
    # # ---这是附件部分---
    # # 类型附件
    # part = MIMEApplication(open(os.path.abspath('/Users/fengjinqi/fsdownload/website_20200910_010000.sql'), 'rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="abc_backup.sql")
    # msg.attach(part)
    # s = smtplib.SMTP("smtp.exmail.qq.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25
    # s.login(_user, _pwd)  # 登陆服务器
    # s.sendmail(_user, _to, msg.as_string())  # 发送邮件
    # s.close();

