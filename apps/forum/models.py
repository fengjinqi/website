import uuid

from django.db import models

# Create your models here.
from django.db.models import Count

from apps.user.models import User

class Forum_plate(models.Model):
    """论坛版块表"""
    name = models.CharField(max_length=64, unique=True, verbose_name="板块名称")
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
        return self.forum_set.count()

    class Meta:
        verbose_name = '论坛版块'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Forum(models.Model):
    """帖子表"""
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    title = models.CharField(max_length = 255, unique = True)
    keywords = models.CharField(max_length=200,verbose_name='关键字',default='',blank=True,null=True)
    # 发布办款-使用外键关联Category
    category = models.ForeignKey(Forum_plate, verbose_name='板块名称',on_delete=models.CASCADE)
    # 文章内容(文章内容可能有很多,所以我们就不用"CharField"来写了,我们用TextField,不用规定他多长了,为可扩展长度)
    content = models.TextField(u"内容")
    click_nums = models.PositiveIntegerField(default=0,verbose_name='阅读数量')
    # 文章作者
    authors = models.ForeignKey(User, verbose_name="作者",on_delete=models.CASCADE)
    # 发布日期
    add_time = models.DateTimeField(auto_now=True, verbose_name="发布日期")
    # 是否隐藏
    hidden = models.BooleanField(default=False, verbose_name="是否隐藏")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '帖子表'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class Priority(models.Model):
    """置顶"""
    stick = models.ForeignKey(Forum,on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="发布日期")

    def __str__(self):
        return self.stick

    class Meta:
        verbose_name = '置顶'
        verbose_name_plural = verbose_name
