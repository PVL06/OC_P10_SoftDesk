from django.contrib.auth import get_user_model
from rest_framework import viewsets

from SoftDeskUser.serializers import UserSerializer
from SoftDeskUser.permissions import UserPermissions


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        return get_user_model().objects.exclude(is_superuser=True)
