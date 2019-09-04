#!/usr/bin/python  
# -*- coding:utf-8 -*-
import datetime

from apps.article.models import Article
from django import template

from apps.forum.models import Forum
from apps.support.models import QQ
from apps.user.models import UserMessage

register = template.Library()
@register.inclusion_tag('pc/base_aside.html')
def get_aside():
    popular = Article.objects.filter(is_show=True).order_by('-click_nums')[:5]
    return {'popular':popular}



@register.simple_tag
def get_categories():
    cur_date = datetime.datetime.now().date()
    yester_day = cur_date - datetime.timedelta(days=30)

    return Article.objects.filter(add_time__gte=yester_day,is_show=True).order_by('-click_nums')[:5]
