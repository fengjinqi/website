#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms

class Article_form(forms.Form):
    title = forms.CharField(required=True,max_length=100)

