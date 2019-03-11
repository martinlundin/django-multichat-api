from django.shortcuts import get_object_or_404
from django.db import models
import uuid as makeuuid
from users.models import Usern
import datetime


def get_chat_by_id(chatid):
    return get_object_or_404(Chat, uuid=chatid)


def is_participant_in_chat(chatid, userid):
    chat = get_object_or_404(Chat, uuid=chatid)
    return chat.participants.filter(uuid=userid).exists()


class Message(models.Model):
    sender = models.ForeignKey(Usern, related_name='sender', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    giphy = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.content)


class Chat(models.Model):
    uuid = models.UUIDField(primary_key=True, default=makeuuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True)
    participants = models.ManyToManyField(Usern, related_name='participants')
    messages = models.ManyToManyField(Message, blank=True)
    timestamp = models.DateTimeField("timestamp", editable=False, default=datetime.datetime.now())

    def save(self, *args, **kw):
        self.timestamp = datetime.datetime.now()
        if "timestamp" in kw:
            kw["timestamp"].append("timestamp")
        super(Chat, self).save(*args, **kw)

    def __str__(self):
        return str(self.uuid)