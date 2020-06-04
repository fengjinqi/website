import uuid

from django.db import models


# Create your models here.
from apps.user.models import User


class dynamic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    image = models.ImageField(upload_to="course/%Y%m%d",blank=True,null=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)
