from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    user_imag = models.ImageField(upload_to='user/%Y/%m/%d',blank=True,default='')
