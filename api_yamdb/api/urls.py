from django.urls import include, path
from rest_framework import routers

from .views import SignUpView, UserViewSet, TokenView, CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)





urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
]