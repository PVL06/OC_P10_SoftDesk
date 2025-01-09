from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from Projects.serializers import ProjectListSerializer
from Projects.models import Project


class ProjectViewset(ModelViewSet):
    
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.all()

    def post(self, request):
        project = Project.objects.create(request.data)
        project.author_id = request.user
        return Response()
        
