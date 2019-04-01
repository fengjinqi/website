#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms

from apps.forum.models import Forum


class Forum_form(forms.ModelForm):
    category = forms.IntegerField(required=True)

    class Meta:
        model = Forum
        fields = ['title','authors','content']

