from rest_framework import serializers

from SoftDeskAPI.models import Project, Issue, Comment, Contributors


class ProjectSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.username', read_only=True)
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'contributors',
            'created_time'
        ]
        extra_kwargs = {
            'created_time': {'read_only': True}
        }

    def get_contributors(self, instance):
        queryset = Contributors.objects.filter(project=instance)
        return [query.contributor.username for query in queryset]


class IssueSerializer(serializers.ModelSerializer):

    author = serializers.CharField(
        source='author.username',
        read_only=True
    )
    assigned_user = serializers.CharField(
        source='assigned_user.username',
        read_only=True
    )
    project = serializers.CharField(
        source='project.name',
        read_only=True
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'name',
            'description',
            'priority',
            'tag',
            'status',
            'author',
            'assigned_user',
            'project',
            'created_time'
        ]
        extra_kwargs = {
            'created_time': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):

    uuid = serializers.UUIDField(
        format='hex',
        read_only=True
    )
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            'description',
            'author',
            'issue_link',
            'created_time'
        ]
        extra_kwargs = {
            'issue_link': {'read_only': True},
            'created_time': {'read_only': True}
        }
