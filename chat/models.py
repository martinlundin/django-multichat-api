from django.shortcuts import get_object_or_404
from django.db import models
import uuid as makeuuid
from users.models import Usern


def get_latest_messages(chatid, from_message=0, to_message=20):
    chat = get_object_or_404(Chat, uuid=chatid)
    return chat.messages.order_by('-timestamp').all()[from_message:to_message]


def get_latest_timestamp(chatid):
    chat = get_object_or_404(Chat, uuid=chatid)
    latest = chat.messages.order_by('-timestamp').all()[:1]
    return latest


def get_current_chat(chatid):
    return get_object_or_404(Chat, uuid=chatid)


def is_participant_in_chat(chatid, userid):
    chat = get_object_or_404(Chat, uuid=chatid)
    return chat.participants.filter(uuid=userid).exists()

class Message(models.Model):
    sender = models.ForeignKey(Usern, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)


class Chat(models.Model):
    uuid = models.UUIDField(primary_key=True, default=makeuuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True)
    participants = models.ManyToManyField(Usern, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return str(self.uuid)