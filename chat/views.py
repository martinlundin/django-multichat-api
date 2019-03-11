from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from rest_framework import generics
from rest_framework import permissions
from chat.models import Chat, Message
from chat.models import is_participant_in_chat
from .serializers import ChatSerializer, ChatDetailSerializer


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(is_participant_in_chat(obj.uuid, request.user.uuid)):
            return True
        else:
            return False


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        uuid = self.request.user
        queryset = uuid.participants.order_by('-timestamp').all()
        return queryset


class ChatDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsParticipant)
