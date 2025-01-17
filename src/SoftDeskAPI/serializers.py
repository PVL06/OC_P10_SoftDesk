from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from SoftDeskAPI.models import User, Project, Issue


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
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
    # todo validation sur le username avec nb de caractère minimum


class ProjectSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'created_time'
        ]
        extra_kwargs = {
            'created_time': {'read_only': True}
        }


class IssueSerializer(serializers.ModelSerializer):

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
            'created_time'
        ]
        extra_kwargs = {
            'author': {'read_only': True},
            'assigned_user': {'read_only': True},
            'created_time': {'read_only': True} 
        }
