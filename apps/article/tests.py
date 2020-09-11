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




