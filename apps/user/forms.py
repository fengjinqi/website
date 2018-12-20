#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms
from captcha.fields import CaptchaField

from apps.user.models import User


class CaptchaTestForm(forms.Form):
    # name = forms.CharField(max_length=100, label='title')
    # password = forms.CharField(max_length=100, label='price')
    captcha = CaptchaField()  # 为生成的验证码图片，以及输入框


class LoginForms(forms.Form):
    telephone = forms.CharField(max_length=11,)
    password = forms.CharField(max_length=16, min_length=6)
    remember = forms.IntegerField(required=False)
    def get_errors(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key,message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}
