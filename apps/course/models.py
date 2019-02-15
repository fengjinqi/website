from django.db import models

# Create your models here.
from apps.user.models import User


class Courses(models.Model):
    """
    课程
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100,verbose_name='课程名字')
    info = models.TextField(verbose_name='介绍')
    image = models.ImageField(upload_to="course/%Y%m%d")
    is_active = models.BooleanField(default=False,verbose_name='状态')#默认False更新中
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)


class CourseList(models.Model):
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name='标题')
    conent = models.TextField(verbose_name='内容')
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程列表'
        verbose_name_plural = verbose_name
