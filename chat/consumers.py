from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Content, get_chat_by_id, is_participant_in_chat
from .serializers import get_latest_messages

User = get_user_model()


def get_current_chatid(self):
    return self.scope['url_route']['kwargs']['chatid']


def get_current_chat(self):
    chatid = get_current_chatid(self)
    return get_chat_by_id(chatid)


def get_current_user(self):
    return self.scope['user']


def get_current_userid(self):
    return self.scope['user'].uuid


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = get_current_chatid(self)

        if(is_participant_in_chat(self.room_name, get_current_userid(self))):
            self.room_group_name = 'chat_%s' % self.room_name
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept(self.scope['subprotocols'][0]) #Because authentication is in subprotocol, we need to user value as parameter
        else:
            self.close()

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def get_messages(self, data):
        messages = get_latest_messages(get_current_chatid(self), data['fromMessage'], data['toMessage'])
        content = {
            'command': 'return_messages',
            'messages': self.return_messages(messages)
        }
        self.send_to_browser(content)

    def return_messages(self, messages):
        result = []
        for message in messages:
            result.append(message)
        return result

    def send_message(self, data):
        content = Content.objects.create(text=data['content'])
        message = Message.objects.create(
            sender=get_current_user(self),
            content=content
        )
        current_chat = get_current_chat(self)
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'send_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_to_browser(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    commands = {
        'get_messages': get_messages,
        'send_message': send_message
    }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )