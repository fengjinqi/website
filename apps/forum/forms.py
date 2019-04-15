#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms

from apps.forum.models import Forum, Parent_Comment


class Forum_form(forms.ModelForm):
    """
    发布帖子
    """
    category = forms.IntegerField(required=True)
    class Meta:
        model = Forum
        fields = ['title','authors','content']

class ParentComment(forms.ModelForm):

    class Meta:
        model = Parent_Comment
        fields = ['comments','user','forums','parent_comments','to_Parent_Comments','url']