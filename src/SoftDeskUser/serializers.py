from django.contrib.auth import password_validation, get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
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