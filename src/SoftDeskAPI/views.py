from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from SoftDeskAPI.serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer
from SoftDeskAPI.permissions import UserPermissions, ProjectPermissions
from SoftDeskAPI.models import User, Project, Contributors, Issue, Comment
from SoftDeskAPI.filters import ProjectFilter, IssueFilter


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True)


class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

    def get_queryset(self):
        return Project.objects.filter(
            project__contributor=self.request.user
        ).order_by('-created_time')
    
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        project = get_object_or_404(Project, pk=serializer.data.get('id'))
        user = get_object_or_404(User, id=self.request.user.pk)
        Contributors.objects.create(project=project, contributor=user)    

    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if request.user != project.author:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        new_contributor = User.get_user_by_username(request.POST.get('username'))
        if Contributors.check_user_in_project(new_contributor, pk):
            return Response(
                {'detail': 'This user is already a contributor'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Contributors.objects.create(project=project, contributor=new_contributor)
        return Response(
            {'detail': f'The user {new_contributor} has been added to the contributors'}
        )

    @action(detail=True, methods=['post'])
    def remove_contributor(self, request, pk=None):
        if request.user != get_object_or_404(Project, pk=pk).author:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        contributor = User.get_user_by_username(request.POST.get('username'))
        if not Contributors.check_user_in_project(contributor, pk):
            return Response(
                {'detail': f'{contributor} is not a contributor for this project'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Contributors.objects.filter(project=pk, contributor=contributor).delete()
        return Response(
            {'detail': f'The user {contributor} has been deleted to the contributors'},
        )


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [ProjectPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IssueFilter

    def get_queryset(self):
        return Issue.objects.filter(
            project=self.kwargs.get('project_pk')
        ).order_by('-created_time')

    @transaction.atomic
    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        assigned_user = User.get_user_by_username(self.request.POST.get('assigned_user'))
        if not Contributors.check_user_in_project(assigned_user, project):
            raise serializers.ValidationError(
                {'detail': f'{assigned_user} is not a contributor to the project'}
            )
        serializer.save(
            project=project,
            author=self.request.user,
            assigned_user=assigned_user
        )


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ProjectPermissions]

    def get_queryset(self):
        return Comment.objects.filter(
            issue=self.kwargs.get('issue_pk')
        ).order_by('-created_time')

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('issue_pk'))
        issue_url = self.request.build_absolute_uri().replace('comment/', '')
        serializer.save(
            author=self.request.user,
            issue=issue,
            issue_link=issue_url
        )
