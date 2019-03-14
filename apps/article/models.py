import uuid
from datetime import datetime


from django.db import models

from apps.user.models import User
# Create your models here.


class Category_Article(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=100)
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """文章"""
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    authors = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    category = models.ForeignKey(Category_Article,on_delete=models.CASCADE,verbose_name='分类')
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200,blank=True,null=True)
    desc = models.CharField(max_length=400,blank=True,null=True)
    list_pic = models.ImageField(upload_to='article/%Y%m%d',blank=True,null=True)
    content = models.TextField()
    click_nums = models.IntegerField(default=0,verbose_name='阅读数量')
    is_show = models.BooleanField(default=True,verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)

    def get_number(self):
        n= self.article_comment_set.all()
        num = self.article_comment_set.all().count()
        for i in n:
            num+=i.articlecommentreply_set.count()
        return num

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Recommend(models.Model):
    recommends = models.ForeignKey(Article,on_delete=models.CASCADE,null=True,)
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    add_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '文章推荐'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Article_Comment(models.Model):
    """"评论"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    article =models.ForeignKey(Article,verbose_name='文章',on_delete=models.CASCADE)
    comments = models.TextField(verbose_name='评论')
    address = models.CharField(max_length=50,verbose_name='地址',blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name ='文章评论'
        verbose_name_plural=verbose_name
        ordering = ('-add_time',)



class ArticleCommentReply(models.Model):
    """评论回复"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='当前用户',related_name='form_uid')
    to_uids = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='目标用户',related_name='to_uids',default='')
    comments = models.TextField(verbose_name='回复内容')
    aomments_id = models.ForeignKey(Article_Comment,on_delete=models.CASCADE,verbose_name='回复id')
    address = models.CharField(max_length=50, verbose_name='地址',blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


class Headlines(models.Model):
    """头条"""
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    title = models.CharField(max_length=200,verbose_name='标题')
    category = models.CharField(max_length=20,verbose_name='分类')
    conent = models.TextField(verbose_name='内容',default='')
    author_name = models.CharField(max_length=100,verbose_name='来源')
    url = models.URLField(verbose_name='地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        ordering = ('-add_time',)