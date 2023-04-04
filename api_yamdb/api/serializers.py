from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'email', 'username', 'bio',
            'role', 'first_name', 'last_name'
        ]
        model = User
        read_only_field = ('role',)
        extra_kwargs = {
            'email': {
                'required': True
            },
            'username': {
                'required': True
            }
        }


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True, validators=[UnicodeUsernameValidator(),])

# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['username', 'email']
#         model = User
#         extra_kwargs = {
#             'email': {
#                 'required': True
#             },
#             'username': {
#                 'required': True
#             }
#         }
#     validators = [
#         UniqueTogetherValidator(
#             queryset=User.objects.all(),
#             fields=['username', 'email']
#         )
#     ]
    def validate(self, data):
        if User.objects.filter(username=data['username'], email=data['email']).exists():
            return data
        if User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Пользователь с таким емайлом существует')
        return data



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


class DictSlugRelatedField(serializers.SlugRelatedField):
    """
    Пользовательское реляционное представление поля с выводом данных в словарь.
    """
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug
        }


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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', many=False
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, 'Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, 'Оценка должна быть не больше 10.')
        ],
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
                request.method == 'POST'
                and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Вы можете оставить только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', many=False
    )
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
