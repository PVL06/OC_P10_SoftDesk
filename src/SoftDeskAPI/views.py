from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from SoftDeskAPI.serializers import UserSerializer
from SoftDeskAPI.permissions import UserPermissions


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        users = get_user_model()
        return users.objects.all()
