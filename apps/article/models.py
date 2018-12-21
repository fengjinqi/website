
from datetime import datetime


from django.db import models

from apps.user.models import User
# Create your models here.

class Category_Article(models.Model):
    name = models.CharField(max_length=100)
    add_time = models.DateTimeField(default=datetime.now)

class Article_add(models.Model):
    authors = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category_Article,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200,blank=True,null=True)
    desc = models.CharField(max_length=400,blank=True,null=True)
    list_pic = models.ImageField(upload_to='article/%Y%m%d',blank=True,null=True)
    content = models.TextField()
    click_nums = models.IntegerField(default=0,verbose_name='阅读数量')
    add_time = models.DateTimeField(auto_now_add=True)


class Article_Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article =models.ForeignKey(Article_add,verbose_name='文章',on_delete=models.CASCADE)
    comments = models.TextField(verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name ='文章评论'
        verbose_name_plural=verbose_name