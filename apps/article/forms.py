#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms

from apps.article.models import Article_add


class Article_form(forms.ModelForm):
    category = forms.IntegerField(required=True)
    class Meta:
        model = Article_add
        fields = ['title','authors','content']

