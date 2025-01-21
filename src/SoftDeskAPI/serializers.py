from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from SoftDeskAPI.models import User, Project, Issue, Comment, Contributors


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError('You must be over 15 years old')
        return value

    def validate_password(self, value):
        try:
            password_validation.validate_password(password=value)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages)
        else:
            return make_password(value)

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('Your username must have at least 4 characters.')
        return value


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
        read_only = True
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
