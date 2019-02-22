from rest_framework import generics
from rest_framework import permissions

from . import models
from . import serializers


class UsernListView(generics.ListAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = models.Usern.objects.all()
        return queryset


class UsernCreateView(generics.CreateAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernCreateSerializer
    permission_classes = (permissions.AllowAny,)


class UsernDetailView(generics.RetrieveAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernSerializer
    permission_classes = (permissions.AllowAny,)


class UsernUpdateView(generics.UpdateAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UsernDeleteView(generics.DestroyAPIView):
    queryset = models.Usern.objects.all()
    serializer_class = serializers.UsernSerializer
    permission_classes = (permissions.IsAuthenticated,)
