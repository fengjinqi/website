#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms
from captcha.fields import CaptchaField

from apps.user.models import User, Follows


class CaptchaTestForm(forms.Form):

    captcha = CaptchaField()  # 为生成的验证码图片，以及输入框


class RegisterForm(forms.ModelForm):
    #captcha = CaptchaField()  # 为生成的验证码图片，以及输入框
    password1 = forms.CharField(max_length=32)
    class Meta:
        model = User
        fields = ['username','email','password']
    def clean(self):
        clend = super(RegisterForm, self).clean()
        password = clend.get('password')
        password1 = clend.get('password1')
        if password != password1:
            self._errors['mssage'] = '两次密码不一样'
            #raise forms.ValidationError(message='两次密码不一样')
        return clend


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

class Follow_Forms(forms.ModelForm):

    class Meta:
        model = Follows
        fields = ['follow',]



