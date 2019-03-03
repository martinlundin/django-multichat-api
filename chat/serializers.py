from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from chat.models import Chat


class ProfileSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('uuid', 'participants')
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

    class Meta:
        model = Chat
        fields = ('uuid', 'name', 'messages', 'participants')
        read_only = ('uuid',)

    #Todo Make it possible to add new participants and remove yourself
