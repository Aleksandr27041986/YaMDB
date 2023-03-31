from datetime import date

from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
