from datetime import datetime

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#from shortuuidfield import ShortUUIDField

class User(AbstractUser):
    #id = ShortUUIDField(primary_key=True)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(max_length=60, blank=True, null=True, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号码',default='')
    user_imag = models.ImageField(upload_to='user/%Y/%m/%d',blank=True,default='',verbose_name='用户头像')
    email = models.EmailField(blank=True,null=True)




class Follow(models.Model):
    """关注表"""
    follow = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow',verbose_name='被关注的，作者')
    fan = models.ForeignKey(User,on_delete=models.CASCADE,related_name='fan',verbose_name='粉丝')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')





class VerifyCode(models.Model):
    """短信验证码"""
    code = models.CharField(verbose_name='验证码',max_length=10)
    mobile = models.CharField(blank=True,null=True,verbose_name='电话',max_length=11)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name='短信验证码'
        verbose_name_plural=verbose_name