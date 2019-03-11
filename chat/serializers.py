from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import Chat, Message
from users.serializers import ChatUsernSerializer
from users.models import Usern
from django.shortcuts import get_object_or_404


def get_latest_messages(chatid, from_message=0, to_message=20):
    chat = get_object_or_404(Chat, uuid=chatid)
    qs = chat.messages.order_by('-timestamp').all()[from_message:to_message]
    return MessageSerializer(qs, many=True, read_only=True).data


def save_message(sender, chat, data):
    message = Message.objects.create(
        sender=sender,
        text=data['content'].get('text', ""),
        giphy=data['content'].get('giphy', ""),
    )
    chat.messages.add(message)
    chat.save()

    return MessageSerializer(message).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    def get_messages(self, chat):
        return get_latest_messages(chat.uuid, 0, 1)

    class Meta:
        model = Chat
        fields = ('uuid', 'name', 'participants', 'messages', 'timestamp')
        read_only = ('uuid',)

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        auth_user = self.context['request'].user

        #Todo also check if chat with participants already exists
        if auth_user in participants:
            chat = Chat()
            chat.save()
            for user in participants:
                chat.participants.add(user)
            chat.save()
            return chat
        else:
            raise ValidationError('You have to be one of the participants')


class ChatDetailSerializer(serializers.ModelSerializer):
    participants = ChatUsernSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'
        read_only = ('uuid',)

    #Todo Make it possible to add new participants and remove yourself
