from django.db import models

# Create your models here.


class Banners(models.Model):
    """
    广告
    """
    title = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(upload_to='support/%Y%m%d',blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    add_time = models.DateTimeField(auto_now_add=True)


class Emails(models.Model):
    qq = models.CharField(max_length=11,blank=True,null=True)
    iphone = models.CharField(max_length=11,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    add_time = models.DateTimeField(auto_now_add=True)


class link(models.Model):
    title =  models.CharField(max_length=100)
    url = models.URLField()
    add_time = models.DateTimeField(auto_now_add=True)