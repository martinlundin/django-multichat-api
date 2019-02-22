from rest_framework import serializers
from . import models
import time


class UsernSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usern
        fields = ('uuid', 'name', 'image')
        read_only_fields = ('uuid',)


class UsernCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usern
        fields = ('uuid', 'email', 'name', 'image')
        read_only_fields = ('uuid',)