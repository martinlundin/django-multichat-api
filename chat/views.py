from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from chat.models import Chat
from chat.models import Usern
from .serializers import ChatSerializer, ChatDetailSerializer


#Todo IMPORTANT check if this is actually a participant, if it is return True. Also put it in a permission.py file and import
#Fine for now, just because chat id is actually random, only the owner should find it through listing their own chats.
class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, uuid=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_current_chat(chatId):
    return get_object_or_404(Chat, uuid=chatId)


class ChatListView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Chat.objects.all()
        uuid = self.request.user
        if uuid is not None:
            queryset = uuid.chats.all()
        return queryset


class ChatDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsParticipant)