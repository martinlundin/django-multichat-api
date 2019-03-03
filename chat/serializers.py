from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import Chat, Message, get_latest_messages, get_latest_timestamp


class ProfileSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', 'content', 'timestamp')


class TimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('timestamp',)



class ChatSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True)
    messages = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    def get_messages(self, chat):
        qs = get_latest_messages(chat.uuid, 20)
        return MessagesSerializer(qs, many=True, read_only=True).data

    #Todo make this not stupid, and not nested
    def get_timestamp(self, chat):
        qs = get_latest_messages(chat.uuid, 1)
        return TimestampSerializer(qs, many=True, read_only=True).data

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
    participants = ProfileSerializer(many=True)
    messages = MessagesSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('uuid', 'name', 'participants', 'messages')
        read_only = ('uuid',)

    #Todo Make it possible to add new participants and remove yourself
