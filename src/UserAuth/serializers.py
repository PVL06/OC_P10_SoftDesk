from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from UserAuth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

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
        

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
        ]
