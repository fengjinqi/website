import uuid
from datetime import datetime

from django.db import models

# Create your models here.
from django.db.models import Count

from apps.user.models import User

class Forum_plate(models.Model):
    """论坛版块表"""
    name = models.CharField(max_length=64, unique=True, verbose_name="板块名称")
    image = models.ImageField(upload_to='forum/%Y%m%d',verbose_name='图标',blank=True)
    # CATEGORY_CHOICES = (
    #     (1, '一级类目'),
    #     (2, '二级类目'),
    #     (3, '三级类目')
    # )
    # code = models.CharField(default='', max_length=30, verbose_name='类别code', help_text='类别code')
    # category_type = models.IntegerField(choices=CATEGORY_CHOICES,default=1, verbose_name='类目级别', help_text='类目级别')
    # parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类目级', help_text='父类目级',
    #                                     related_name='sub_cat', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE,default=uuid.uuid4)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def get_count(self):
        return self.forum_set.filter(hidden=False).count()

    class Meta:
        verbose_name = '论坛版块'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Forum(models.Model):
    """帖子表"""
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    title = models.CharField(max_length = 255, unique = True)
    keywords = models.CharField(max_length=200,verbose_name='关键字',default='',blank=True,null=True)
    category = models.ForeignKey(Forum_plate, verbose_name='板块名称',on_delete=models.CASCADE)
    content = models.TextField(u"内容")
    click_nums = models.PositiveIntegerField(default=0,verbose_name='阅读数量')
    authors = models.ForeignKey(User, verbose_name="作者",on_delete=models.CASCADE)
    # 发布日期
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="发布日期")
    # 是否关闭
    hidden = models.BooleanField(default=False, verbose_name="是否隐藏")

    def __str__(self):
        return self.title

    def get_number(self):
        n = self.comment_set.all()
        num = self.comment_set.all().count()
        for i in n:
            num += i.parent_comment_set.count()
        return num

    class Meta:
        verbose_name = '帖子表'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Forum_click(models.Model):
    """帖子浏览量"""
    forums = models.ForeignKey(Forum, verbose_name='帖子', on_delete=models.CASCADE)
    thumbs = models.IntegerField(default=0)
    models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.forums


class Comment(models.Model):
    """评论"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论人')
    forums = models.ForeignKey(Forum, verbose_name='帖子', on_delete=models.CASCADE)
    comments = models.TextField(verbose_name='评论')
    address = models.CharField(max_length=50, verbose_name='地址', blank=True, null=True)
    url = models.CharField(max_length=60, blank=True, null=True, default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = '帖子评论表'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Parent_Comment(models.Model):
    """评论回复"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='当前用户',related_name='form_Parent_Comment')
    to_Parent_Comments = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='目标用户',related_name='to_Parent_Commenty',default='')
    forums = models.ForeignKey(Forum, verbose_name='帖子', on_delete=models.CASCADE)
    comments = models.TextField(verbose_name='评论')
    parent_comments = models.ForeignKey(Comment,blank=True,null=True,on_delete=models.CASCADE)
    address = models.CharField(max_length=50, verbose_name='地址', blank=True, null=True)
    url = models.CharField(max_length=60, blank=True, null=True, default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = '帖子回复表'
        verbose_name_plural = verbose_name



class Priority(models.Model):
    """置顶"""
    stick = models.ForeignKey(Forum,on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="发布日期")

    def __str__(self):
        return self.stick

    class Meta:
        verbose_name = '置顶'
        verbose_name_plural = verbose_name
