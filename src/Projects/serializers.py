from rest_framework import serializers

from Projects.models import Project

class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'project_name',
            'description',
            'type',
            'created_time',
        ]

    def create(self, validated_data):
        project = Project.objects.create(
            project_name=validated_data['project_name'],
            description=validated_data['description'],
            type = validated_data['type'],
            author = self.context.get('request').user
        )
        project.save()
        return project
