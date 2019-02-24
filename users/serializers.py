from rest_framework import serializers
from . import models
from rest_framework.authtoken.models import Token

class UsernSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usern
        fields = ('uuid', 'username', 'name', 'image')
        read_only_fields = ('uuid', 'username')



class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')