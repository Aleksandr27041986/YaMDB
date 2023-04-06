from django.db.models import Avg
from requests import Response

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import TitleFilterSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModAuthorOrReadOnly)
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer,
                          SignUpSerializer, UserSerializer, TokenSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    lookup_field = 'username'
    search_fields = ['username', ]

    @action(methods=['patch', 'get'],
            permission_classes=[IsAuthenticated],
            detail=False)
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)

        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)

        return Response(serializer.data)


def email_send(email, user):
    send_mail(
        subject='YaMDB Confirmation Code',
        message=f'Hello, {user.username}! \nYour confirmation code: '
                f'{user.confirmation_code}',
        from_email=settings.EMAIL_HOST,
        recipient_list=[email],
        fail_silently=False
    )


class SignUpView(views.APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username, email=email)
            email_send(user.email, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.create(username=username, email=email)
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()
            email_send(user.email, user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


class TokenView(views.APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            try:
                user = get_object_or_404(User, username=username)
            except User.DoesNotExist:
                return Response(
                    {
                        'email': 'Not found'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            confirm_code = serializer.validated_data.get('confirmation_code')
            if confirm_code == user.confirmation_code:
                token = AccessToken.for_user(user)
                return Response(
                    {
                        'token': str(token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    "Неверный confirmation code!",
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый вьюсет для отображения списка объектов, добавления и удаления
    объекта, с функцией поиска по полю.
    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.get_queryset().order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.get_queryset().order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete', ]
    filterset_class = TitleFilterSet


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModAuthorOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModAuthorOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
