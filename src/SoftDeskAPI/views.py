from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from SoftDeskAPI.serializers import UserSerializer, ProjectSerializer
from SoftDeskAPI.permissions import UserPermissions, ProjectPermissions
from SoftDeskAPI.models import Project, Contributors


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        user_model = get_user_model()
        return user_model.objects.all()


class ProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]

    def get_queryset(self):
        project = Project.objects.all()
        return project
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        project = get_object_or_404(Project, pk=serializer.data.get('id'))
        user = get_object_or_404(get_user_model(), id=self.request.user.pk)
        Contributors.objects.create(
            project_id=project,
            contributor_id=user
        )


    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk):
        new_contributor = get_object_or_404(
            get_user_model(),
            username=request.POST.get('username')
        )
        project_contributors = Contributors.objects.filter(project_id=pk)
        if new_contributor not in project_contributors:
            return response.Response({'test': project_contributors[0].contributor_id.pk,
                                      'new contrib pk': new_contributor.pk,
                                      'project pk': pk,
                                      })
        return response.Response({'status': 'failed'})
