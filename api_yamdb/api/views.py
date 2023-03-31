from requests import Response
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.filters import OrderingFilter

from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)
from .filters import TitleFilterSet
from reviews.models import Category, Genre, Title


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый вьюсет для отображения списка объектов, добавления и удаления
    объекта и с функцией поиска по полю.
    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete', ]
    filterset_class = TitleFilterSet



