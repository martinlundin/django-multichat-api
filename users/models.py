from django.db import models
import uuid as makeuuid
import os
from django.contrib.auth.models import AbstractUser


def get_image_path(instance, filename):
    return os.path.join('users', str(instance.uuid), filename)


class Usern(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=makeuuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=get_image_path, default="/general/default-profile.png")
    online = models.BooleanField(default=False)

    def __str__(self):
        return str(self.uuid)
