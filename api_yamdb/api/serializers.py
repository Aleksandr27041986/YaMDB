from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from reviews.models import Category, Genre, Title


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


class DictSlugRelatedField(serializers.SlugRelatedField):
    """
    Пользовательское реляционное представление поля с выводом данных в словарь.
    """
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug
        }


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        fields = ['username', 'confirmation_code']
        model = User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = DictSlugRelatedField(slug_field='slug',
                                    queryset=Category.objects.all(),
                                    required=True)
    genre = DictSlugRelatedField(slug_field='slug',
                                 queryset=Genre.objects.all(), many=True,
                                 required=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError('Не верный год выпуска.')
        return value
