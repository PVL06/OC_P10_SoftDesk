from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from SoftDeskAPI.serializers import UserSerializer, ProjectSerializer, IssueSerializer
from SoftDeskAPI.permissions import UserPermissions, ProjectPermissions
from SoftDeskAPI.models import User, Project, Contributors, Issue


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    #todo voir si besoin d'une fonction pour les filtres sinon repasser en queryset = User.objects.all()
    def get_queryset(self):
        return User.objects.all()


class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]

    queryset = Project.objects.all()
    
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        project = get_object_or_404(Project, pk=serializer.data.get('id'))
        user = get_object_or_404(User, id=self.request.user.pk)
        Contributors.objects.create(project_id=project, contributor_id=user)    

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
        Contributors.objects.create(project_id=project, contributor_id=new_contributor)
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
        Contributors.objects.filter(project_id=pk, contributor_id=contributor).delete()
        return Response(
            {'detail': f'The user {contributor} has been deleted to the contributors'},
        )


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    queryset = Issue.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        serializer.save(
            project=Project.objects.get(pk=project_id),
            author=self.request.user,
            assigned_user=self.request.user
        )