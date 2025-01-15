from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from SoftDeskAPI.serializers import UserSerializer, ProjectSerializer
from SoftDeskAPI.permissions import UserPermissions, ProjectPermissions
from SoftDeskAPI.models import Project, Contributors


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        user_model = get_user_model()
        return user_model.objects.all()


class ProjectActions:
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if request.user != project.author:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        new_contributor = get_object_or_404(get_user_model(), username=request.POST.get('username'))
        if self._check_user_in_project(new_contributor, pk):
            return Response(
                {'detail': 'This user is already a contributor'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Contributors.objects.create(project_id=project, contributor_id=new_contributor)
        return Response(
            {'detail': f'The user {new_contributor} has been added to the contributors'}
        )

    @action(detail=True, methods=['post'])
    def remove_contributor(self, request, pk=None):
        if request.user != get_object_or_404(Project, pk=pk).author:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        contributor = get_object_or_404(get_user_model(), username=request.POST.get('username'))
        if not self._check_user_in_project(contributor, pk):
            return Response(
                {'detail': f'{contributor} is not a contributor for this project'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Contributors.objects.filter(project_id=pk, contributor_id=contributor).delete()
        return Response(
            {'detail': f'The user {contributor} has been deleted to the contributors'},
        )

    @staticmethod
    def _check_user_in_project(user, pk):
        return Contributors.objects.filter(project_id=pk, contributor_id=user).exists()


class ProjectViewset(viewsets.ModelViewSet, ProjectActions):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]

    def get_queryset(self):
        project = Project.objects.all()
        return project
    
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        project = get_object_or_404(Project, pk=serializer.data.get('id'))
        user = get_object_or_404(get_user_model(), id=self.request.user.pk)
        Contributors.objects.create(project_id=project, contributor_id=user)