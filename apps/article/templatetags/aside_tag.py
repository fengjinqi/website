#!/usr/bin/python  
# -*- coding:utf-8 -*-
from apps.article.models import Article
from django import template

from apps.user.models import UserMessage

register = template.Library()
@register.inclusion_tag('pc/base_aside.html')
def get_aside():
    popular = Article.objects.all().order_by('-click_nums')[:5]
    return {'popular':popular}

@register.simple_tag
def get_categories():
    return Article.objects.all().order_by('-click_nums')[:5]
