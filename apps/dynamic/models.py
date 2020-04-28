import uuid

from django.db import models


# Create your models here.


class dynamic(models):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

