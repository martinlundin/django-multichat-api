from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import Chat, Message, Content
from users.serializers import ChatUsernSerializer
from django.shortcuts import get_object_or_404


def get_latest_messages(chatid, from_message=0, to_message=20):
    chat = get_object_or_404(Chat, uuid=chatid)
    qs = chat.messages.order_by('-timestamp').all()[from_message:to_message]
    return MessageSerializer(qs, many=True, read_only=True).data

def save_message(user, content):
    Message.objects.create(
        sender=user,
        content=content
    )

def get_latest_timestamp(chatid):
    chat = get_object_or_404(Chat, uuid=chatid)
    qs = chat.messages.order_by('-timestamp').all()[:1]
    return TimestampSerializer(qs, many=True, read_only=True).data


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('text', 'giphy')


class MessageSerializer(serializers.ModelSerializer):
    sender = ChatUsernSerializer(read_only=True)
    content = ContentSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('sender', 'content', 'timestamp')


class TimestampSerializer(serializers.ModelSerializer):
    #Todo make this not stupid, it should return string of timestamp
    class Meta:
        model = Message
        fields = ('timestamp',)


class ChatSerializer(serializers.ModelSerializer):
    participants = ChatUsernSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    def get_messages(self, chat):
        return get_latest_messages(chat.uuid)

    def get_timestamp(self, chat):
        return get_latest_timestamp(chat.uuid)

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
        fields = ('uuid', 'name', 'participants', 'messages')
        read_only = ('uuid',)

    #Todo Make it possible to add new participants and remove yourself
