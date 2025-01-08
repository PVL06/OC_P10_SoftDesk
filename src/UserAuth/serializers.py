from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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

    def create(self, validated_data):
        try:
            validate_password(password=validated_data['password'])
        except ValidationError as error:
            raise serializers.ValidationError({'password': error.messages})
        else:
            new_user = User.objects.create(
                username=validated_data['username'],
                age=validated_data['age'],
                can_be_contacted=validated_data['can_be_contacted'],
                can_data_be_shared=validated_data['can_data_be_shared']
            )

            new_user.set_password(validated_data['password'])
            new_user.save()
            return new_user
