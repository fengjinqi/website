import uuid
from datetime import datetime

from django.db import models

# Create your models here.
from apps.user.models import User


class dynamic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    name = models.ManyToManyField("dynamicCategory")
    image = models.ImageField(upload_to="course/%Y%m%d", blank=True, null=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    location = models.CharField(max_length=50, verbose_name="位置")
    add_time = models.DateTimeField(auto_now_add=True)

    def get_number(self):
        n = self.dynamiccomment_set.all()
        num = self.dynamiccomment_set.count()
        for i in n:
            num += i.dynamiccommentreply_set.count()
        return num

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '话题'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class dynamicCategory(models.Model):
    title = models.CharField(max_length=256, verbose_name="话题")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '话题'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class dynamicComment(models.Model):
    """"评论"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    dynamic = models.ForeignKey(dynamic, verbose_name='话题', on_delete=models.CASCADE)
    comments = models.TextField(verbose_name='评论')
    url = models.CharField(max_length=60, blank=True, null=True, default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.dynamic.content

    class Meta:
        verbose_name = '话题评论'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class dynamicCommentReply(models.Model):
    """评论回复"""
    dynamicUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='当前用户', related_name='dynamicUser')
    dynamicToUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='目标用户', related_name='dynamicToUser',
                                      default='')
    comments = models.TextField(verbose_name='回复内容')
    url = models.CharField(max_length=60, blank=True, null=True, default='')
    aomments_id = models.ForeignKey(dynamicComment, on_delete=models.CASCADE, verbose_name='回复id')
    address = models.CharField(max_length=50, verbose_name='地址', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
