from django.db import models
import uuid as makeuuid
import os
from django.contrib.auth.models import AbstractUser


def get_image_path(instance, filename):
    return os.path.join('uploads/users', str(instance.id), filename)


class Usern(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=makeuuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.email