#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms

from apps.forum.models import Forum, Parent_Comment


class Forum_form(forms.ModelForm):
    """
    发布帖子
    """
    category = forms.IntegerField(required=True)
    keywords = forms.CharField(max_length=200,required=False,error_messages={"max_length":'字段不能超过200'})
    title = forms.CharField(required=True, max_length=255, error_messages={"max_length": '字段不能超过255'})

    class Meta:
        model = Forum
        fields = ['authors','content']


class ParentComment(forms.ModelForm):

    class Meta:
        model = Parent_Comment
        fields = ['comments','user','forums','parent_comments','to_Parent_Comments','url']