from rest_framework import generics
from rest_framework import permissions
from . import models
from . import serializers


#Is this the right place to add permission classes?
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return str(obj.uuid) == str(request.user)


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