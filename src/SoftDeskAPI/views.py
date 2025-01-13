from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from SoftDeskAPI.serializers import UserSerializer, ProjectSerializer
from SoftDeskAPI.permissions import UserPermissions, ProjectPermissions
from SoftDeskAPI.models import Project


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        users = get_user_model()
        return users.objects.all()


class ProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]

    def get_queryset(self):
        project = Project.objects.all()
        return project
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
