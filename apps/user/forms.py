#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms
from captcha.fields import CaptchaField
class CaptchaTestForm(forms.Form):
    # name = forms.CharField(max_length=100, label='title')
    # password = forms.CharField(max_length=100, label='price')
    captcha = CaptchaField()  # 为生成的验证码图片，以及输入框