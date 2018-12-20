
from datetime import datetime


from django.db import models

from apps.user.models import User
# Create your models here.



class Article_add(models.Model):
    authors = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200,blank=True,null=True)
    desc = models.CharField(max_length=400,blank=True,null=True)
    list_pic = models.ImageField(upload_to='article/list_pic/%Y/%m/%d',blank=True,null=True)
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)


