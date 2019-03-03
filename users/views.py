from rest_framework import generics
from rest_framework import permissions
from . import models
from . import serializers
from .permissions import IsOwnerOrReadOnly


class UsernListView(generics.ListAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = models.Usern.objects.all()
        return queryset


class UsernDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)