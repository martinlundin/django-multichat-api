from rest_framework import serializers
from . import models
from rest_framework.authtoken.models import Token
from drf_extra_fields.fields import Base64ImageField


class ChatUsernSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usern
        fields = ('uuid', 'name', 'image')


class UsernSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = models.Usern
        fields = ('uuid', 'username', 'name', 'image')
        read_only_fields = ('uuid', 'username')

    def update(self, instance, validated_data):
        instance.image = validated_data.pop('image')
        instance.name = validated_data.pop('name')
        instance.save()
        return instance


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')