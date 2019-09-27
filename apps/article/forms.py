#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms

from apps.article.models import Article


class Article_form(forms.ModelForm):
    category = forms.IntegerField(required=True)
    desc = forms.CharField(required=False,max_length=256,error_messages={"max_length":'字段不能超过256'})
    keywords = forms.CharField(required=False,max_length=200,error_messages={"max_length":'字段不能超过200'})
    title = forms.CharField(required=True,max_length=100,error_messages={"max_length":'字段不能超过100'})

    class Meta:
        model = Article
        fields = ['authors','content']

