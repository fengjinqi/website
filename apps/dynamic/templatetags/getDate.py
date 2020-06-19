#!/usr/bin/python  
# -*- coding:utf-8 -*-  
# @Time    : 2020/6/19 2:36 下午
# @Author  : fengjinqi
# @Email   : 1218525402@qq.com
# @File    : getDate.py
# @Software: PyCharm
from django import template
from datetime import datetime
register = template.Library()

@register.filter
def getTimer(tiem):
    current_timer = datetime.now()
    datetime.now().year
    if current_timer.year==datetime.date(tiem).year and \
            current_timer.year == datetime.date(tiem).year and \
            current_timer.minute == datetime.date(tiem).month:
        return "刚刚"
    print(datetime.now())
    print(datetime.now().day)
    print(datetime.date(tiem).day)
    print(tiem)
    return ""