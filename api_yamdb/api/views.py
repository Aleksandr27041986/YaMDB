from requests import Response
from rest_framework import filters
from rest_framework import mixins
from django.shortcuts import get_object_or_404
# from rest_framework.filters import OrderingFilter
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer)
from .filters import TitleFilterSet
from reviews.models import Category, Genre, Review, Title
# from .permissions import IsAuthorOrAdminOrReadOnly
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, views, status
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .serializers import SignUpSerializer, UserSerializer, TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdmin]
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    search_fields = ['username']
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        else:
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )


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

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        user = get_object_or_None(User, **serializer.initial_data)
        if user is not None:
            email_send(user.email, user)
            return Response(
                f'Письмо с кодом регистрации отправлено на почту {user.email}',
                status=status.HTTP_200_OK
            )
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            user = User.objects.create(
                username=username,
                email=email
            )
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()
            email_send(user.email, user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenView(views.APIView):
    queryset = User.objects.all()

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
    объекта и с функцией поиска по полю.
    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.get_queryset().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.get_queryset().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.get_queryset().order_by('id')
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete', ]
    filterset_class = TitleFilterSet


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
<<<<<<< HEAD
        serializer.save(author=self.request.user, review=review)
=======
        serializer.save(author=self.request.user, review=review)
>>>>>>> develop
