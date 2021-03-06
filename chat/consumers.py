from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, get_chat_by_id, is_participant_in_chat
from .serializers import get_latest_messages, save_message
from users.models import Usern
from fcm_django.models import FCMDevice



def get_current_chatid(self):
    return self.scope['url_route']['kwargs']['chatid']

def get_current_chat(self):
    chatid = get_current_chatid(self)
    return get_chat_by_id(chatid)


def get_current_user(self):
    return self.scope['user']


def get_current_userid(self):
    return self.scope['user'].uuid

def user_is_online(userid):
    Usern.objects.filter(uuid=userid).update(online=True)

def user_is_offline(userid):
    Usern.objects.filter(uuid=userid).update(online=False)


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
            user_is_online(get_current_userid(self))
        else:
            self.close()

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def return_messages(self, messages):
        result = []
        for message in messages:
            result.append(message)
        return result

    def send_message(self, data):
        message = save_message(get_current_user(self), get_current_chat(self), data)
        content = {
            'command': 'send_message',
            'chatid': get_current_chatid(self),
            'message': message
        }

        #All participants that are offline get pushnotifications
        participants_offline = get_current_chat(self).participants.filter(online=False)
        for participant in participants_offline:
            device = FCMDevice.objects.filter(user=participant).first()
            if device:
                device.send_message(get_current_user(self).name, message["text"])

        return self.send_to_channel_layer(content)

    def send_to_channel_layer(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_to_browser_event',
                'message': message
            }
        )

    def send_to_browser(self, message):
        self.send(text_data=json.dumps(message))

    def send_to_browser_event(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    commands = {
        'send_message': send_message
    }

    def disconnect(self, close_code):
        user_is_offline(get_current_userid(self))
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )