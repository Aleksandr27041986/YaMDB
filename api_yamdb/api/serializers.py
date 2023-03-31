from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'email', 'username', 'bio',
            'role', 'first_name', 'last_name'
        ]
        model = User
        extra_kwargs = {
            'email': {
                'required': True
            },
            'username': {
                'required': True
            }
        }


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email']
        model = User
        extra_kwargs = {
            'email': {
                'required': True
            },
            'username': {
                'required': True
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, username):
        if username == 'me'.lower():
            raise ValidationError('Никнейм "me" недоступен!')
        return username


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        fields = ['username', 'confirmation_code']
        model = User