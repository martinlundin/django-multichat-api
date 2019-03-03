from django.db import models
import uuid as makeuuid
from users.models import Usern


class Message(models.Model):
    sender = models.ForeignKey(Usern, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    '''
    def __str__(self):
        return self.users.user.email
    '''

class Chat(models.Model):
    uuid = models.UUIDField(primary_key=True, default=makeuuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True)
    participants = models.ManyToManyField(Usern, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return str(self.uuid)